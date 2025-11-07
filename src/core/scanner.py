import asyncio
import aiohttp
import concurrent.futures
from typing import Dict, List, Any
import json
import re
from ..modules.social_scan import SocialMediaScanner
from ..modules.breach_scan import BreachScanner
from ..modules.number_analysis import NumberAnalyzer
from ..modules.advanced_osint import AdvancedOSINT
from ..utils.logger import Logger

class AdvancedPhoneScanner:
    def __init__(self):
        self.logger = Logger()
        self.social_scanner = SocialMediaScanner()
        self.breach_scanner = BreachScanner()
        self.number_analyzer = NumberAnalyzer()
        self.advanced_osint = AdvancedOSINT()
        self.config = {}
        self.timeout = 30
        self.max_threads = 5
        
    def set_config(self, config: Dict):
        """تعيين تكوين الماسح الضوئي"""
        self.config = config
        self.social_scanner.set_config(config)
        self.breach_scanner.set_config(config)
        
    def set_timeout(self, timeout: int):
        """تعيين مهلة الاتصال"""
        self.timeout = timeout
        
    def set_threads(self, threads: int):
        """تعيين عدد الثreads"""
        self.max_threads = threads
    
    async def async_scan(self, phone_number: str, scan_type: str) -> Dict:
        """مسح غير متزامن"""
        try:
            if scan_type == 'social_media':
                return await self.social_scanner.deep_scan(phone_number)
            elif scan_type == 'breaches':
                return await self.breach_scanner.comprehensive_check(phone_number)
            elif scan_type == 'geolocation':
                return await self.number_analyzer.advanced_analysis(phone_number)
            elif scan_type == 'telegram':
                return await self.social_scanner.scan_telegram(phone_number)
            elif scan_type == 'whatsapp':
                return await self.social_scanner.scan_whatsapp(phone_number)
            elif scan_type == 'darkweb':
                return await self.breach_scanner.darkweb_scan(phone_number)
            else:
                return {}
        except Exception as e:
            self.logger.error(f"خطأ في المسح {scan_type}: {str(e)}")
            return {}
    
    def comprehensive_scan(self, phone_number: str, scan_types: List[str]) -> Dict:
        """مسح شامل متعدد الخيوط"""
        self.logger.info(f"بدء المسح الشامل لأنواع: {', '.join(scan_types)}")
        
        # المعلومات الأساسية أولاً
        results = {
            'scan_info': {
                'phone_number': phone_number,
                'timestamp': str(asyncio.get_event_loop().time()),
                'scan_types': scan_types,
                'version': 'PhoneInfoga Pro 2.0'
            },
            'basic_info': self.number_analyzer.comprehensive_analysis(phone_number)
        }
        
        # المسح غير المتزامن
        async def run_all_scans():
            tasks = []
            for scan_type in scan_types:
                task = self.async_scan(phone_number, scan_type)
                tasks.append(task)
            
            scan_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, scan_type in enumerate(scan_types):
                if not isinstance(scan_results[i], Exception):
                    results[scan_type] = scan_results[i]
        
        # تشغيل المسح غير المتزامن
        try:
            asyncio.run(run_all_scans())
        except RuntimeError:
            # إذا كان هناك loop نشط بالفعل
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_all_scans())
            loop.close()
        
        # إضافة التقييم النهائي
        results['risk_assessment'] = self._calculate_risk_assessment(results)
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _calculate_risk_assessment(self, results: Dict) -> Dict:
        """حساب تقييم المخاطر"""
        risk_score = 0
        factors = []
        
        # تحليل التسريبات
        if results.get('breaches', {}).get('count', 0) > 0:
            risk_score += 30
            factors.append("العثور على الرقم في قواعد بيانات متسربة")
        
        # تحليل وسائل التواصل
        social_media = results.get('social_media', {})
        if social_media.get('profiles_found', 0) > 3:
            risk_score += 20
            factors.append("وجود الرقم في العديد من وسائل التواصل")
        
        # تحليل السمعة
        reputation = results.get('basic_info', {}).get('reputation', {})
        if reputation.get('spam_reports', 0) > 5:
            risk_score += 25
            factors.append("تقرير عن الرقم كمصدر مزعج")
        
        # تحديد مستوى الخطورة
        if risk_score >= 70:
            risk_level = "مرتفع"
        elif risk_score >= 40:
            risk_level = "متوسط"
        else:
            risk_level = "منخفض"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'factors': factors,
            'description': self._get_risk_description(risk_level)
        }
    
    def _get_risk_description(self, level: str) -> str:
        """الحصول على وصف مستوى الخطورة"""
        descriptions = {
            'منخفض': "الرقم يبدو آمناً مع وجود حد أدنى من المخاطر",
            'متوسط': "الرقم لديه بعض المؤشرات التي تستدعي الانتباه",
            'مرتفع': "الرقم لديه مؤشرات خطيرة متعددة"
        }
        return descriptions.get(level, "غير معروف")
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """توليد توصيات أمنية"""
        recommendations = []
        risk_level = results.get('risk_assessment', {}).get('level', 'منخفض')
        
        if risk_level in ['متوسط', 'مرتفع']:
            recommendations.extend([
                "تفعيل التحقق بخطوتين على جميع الحسابات",
                "مراجعة إعدادات الخصوصية على وسائل التواصل",
                "تغيير كلمات المرور المرتبطة بهذا الرقم",
                "مراقبة الحسابات المصرفية لاكتشاف أي نشاط مشبوه"
            ])
        
        if results.get('breaches', {}).get('count', 0) > 0:
            recommendations.append("استخدام Have I Been Pwned للتحقق من التسريبات")
        
        recommendations.extend([
            "عدم مشاركة الرقم مع مواقع غير موثوقة",
            "استخدام تطبيقات المراسلة المشفرة",
            "تفعيل خيارات الخصوصية المتقدمة"
        ])
        
        return recommendations
