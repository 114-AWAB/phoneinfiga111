#!/usr/bin/env python3
"""
PhoneInfoga Pro - النسخة المتطورة
أداة متقدمة لجمع معلومات الهواتف من مصادر مفتوحة
"""

import argparse
import sys
import json
from datetime import datetime
from src.core.scanner import AdvancedPhoneScanner
from src.utils.logger import Logger
from src.utils.export import ReportExporter

class PhoneInfogaPro:
    def __init__(self):
        self.logger = Logger()
        self.scanner = AdvancedPhoneScanner()
        self.exporter = ReportExporter()
        
    def banner(self):
        """عرض شعار البرنامج"""
        banner = """
        ╔═══════════════════════════════════════════╗
        ║           📱 PHONEINFOGA PRO 📱           ║
        ║     النسخة المتطورة - جمع معلومات الهواتف    ║
        ║           لأغراض تعليمية وأمنية            ║
        ╚═══════════════════════════════════════════╝
        """
        print(banner)
    
    def parse_arguments(self):
        """تحليل وسيطات الأوامر"""
        parser = argparse.ArgumentParser(description='PhoneInfoga Pro - أداة متقدمة لجمع معلومات الهواتف')
        
        parser.add_argument('phone', help='رقم الهاتف المستهدف (مثال: +1234567890)')
        
        parser.add_argument('-o', '--output', help='حفظ النتائج في ملف',
                          choices=['json', 'html', 'pdf', 'txt'], default='txt')
        
        parser.add_argument('-d', '--deep-scan', action='store_true',
                          help='مسح عميق (يأخذ وقت أطول)')
        
        parser.add_argument('-s', '--social-media', action='store_true',
                          help='مسح وسائل التواصل الاجتماعي المتقدم')
        
        parser.add_argument('-b', '--breaches', action='store_true',
                          help='فحص قواعد البيانات المتسربة')
        
        parser.add_argument('-g', '--geolocation', action='store_true',
                          help='تحديد الموقع الجغرافي')
        
        parser.add_argument('-a', '--all', action='store_true',
                          help='تشغيل جميع الفحوصات')
        
        parser.add_argument('--api-keys', help='ملف مفاتيح API',
                          default='api_keys.json')
        
        parser.add_argument('--threads', type=int, default=5,
                          help='عدد الثreads للمسح المتوازي')
        
        parser.add_argument('--timeout', type=int, default=30,
                          help='المهلة للاتصالات (بالثواني)')
        
        return parser.parse_args()
    
    def load_config(self, api_keys_file):
        """تحميل التكوين ومفاتيح API"""
        try:
            with open(api_keys_file, 'r') as f:
                return json.load(f)
        except:
            self.logger.warning(f"لم يتم العثور على ملف {api_keys_file}")
            return {}
    
    def run_scan(self, args):
        """تشغيل المسح الشامل"""
        self.logger.info(f"بدء المسح للرقم: {args.phone}")
        
        # تحميل التكوين
        config = self.load_config(args.api_keys)
        
        # إعداد الماسح الضوئي
        self.scanner.set_config(config)
        self.scanner.set_timeout(args.timeout)
        self.scanner.set_threads(args.threads)
        
        # تحديد الفحوصات المطلوبة
        scans_to_run = []
        
        if args.all or args.social_media:
            scans_to_run.extend(['social_media', 'telegram', 'whatsapp'])
        
        if args.all or args.breaches:
            scans_to_run.extend(['breaches', 'darkweb'])
        
        if args.all or args.geolocation:
            scans_to_run.extend(['geolocation', 'carrier'])
        
        if args.deep_scan:
            scans_to_run.extend(['deep_web', 'forums', 'archives'])
        
        # تشغيل المسح
        results = self.scanner.comprehensive_scan(args.phone, scans_to_run)
        
        return results
    
    def main(self):
        """الدالة الرئيسية"""
        self.banner()
        args = self.parse_arguments()
        
        try:
            # تشغيل المسح
            results = self.run_scan(args)
            
            # عرض النتائج
            self.display_results(results)
            
            # تصدير النتائج إذا طُلب
            if args.output:
                filename = self.exporter.export(results, args.output, args.phone)
                self.logger.success(f"تم حفظ النتائج في: {filename}")
                
        except KeyboardInterrupt:
            self.logger.error("تم إيقاف المسح بواسطة المستخدم")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"حدث خطأ: {str(e)}")
            sys.exit(1)
    
    def display_results(self, results):
        """عرض النتائج بشكل منظم"""
        print("\n" + "="*60)
        print("📊 نتائج المسح الشامل")
        print("="*60)
        
        # المعلومات الأساسية
        if 'basic_info' in results:
            self._display_basic_info(results['basic_info'])
        
        # وسائل التواصل
        if 'social_media' in results:
            self._display_social_media(results['social_media'])
        
        # التسريبات
        if 'breaches' in results:
            self._display_breaches(results['breaches'])
        
        # المعلومات الجغرافية
        if 'geolocation' in results:
            self._display_geolocation(results['geolocation'])
        
        # التوصيات
        self._display_recommendations(results)

if __name__ == "__main__":
    app = PhoneInfogaPro()
    app.main()
