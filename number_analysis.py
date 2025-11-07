import phonenumbers
from phonenumbers import carrier, timezone, geocoder
import re
import json
from typing import Dict

class NumberAnalyzer:
    def __init__(self):
        self.carrier_db = self._load_carrier_database()
        self.country_codes = self._load_country_codes()
    
    def comprehensive_analysis(self, phone_number: str) -> Dict:
        """تحليل شامل للرقم"""
        try:
            # استخدام مكتبة phonenumbers للتحليل الدقيق
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # المعلومات الأساسية
            basic_info = {
                'valid': phonenumbers.is_valid_number(parsed_number),
                'format_international': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'format_national': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                'country_code': parsed_number.country_code,
                'national_number': parsed_number.national_number,
                'country': self._get_country_name(parsed_number.country_code),
                'carrier': carrier.name_for_number(parsed_number, "en"),
                'timezones': timezone.time_zones_for_number(parsed_number),
                'location': geocoder.description_for_number(parsed_number, "en"),
                'number_type': self._get_number_type(parsed_number),
                'reputation': self._check_reputation(phone_number)
            }
            
            # التحليل المتقدم
            advanced_analysis = {
                'possible_services': self._identify_possible_services(phone_number),
                'risk_factors': self._identify_risk_factors(phone_number),
                'privacy_score': self._calculate_privacy_score(phone_number),
                'carrier_info': self._get_carrier_info(basic_info['carrier']),
                'country_risk': self._get_country_risk(basic_info['country_code'])
            }
            
            return {**basic_info, **advanced_analysis}
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _get_number_type(self, parsed_number) -> str:
        """تحديد نوع الرقم"""
        number_types = {
            'FIXED_LINE': 'هاتف ثابت',
            'MOBILE': 'هاتف محمول',
            'VOIP': 'صوت عبر الإنترنت',
            'TOLL_FREE': 'مجاني',
            'PREMIUM_RATE': 'مميز',
            'SHARED_COST': 'تكلفة مشتركة',
            'PERSONAL_NUMBER': 'رقم شخصي',
            'UAN': 'رقم وصول عالمي',
            'UNKNOWN': 'غير معروف'
        }
        
        number_type = phonenumbers.number_type(parsed_number)
        return number_types.get(number_type.name, 'غير معروف')
    
    def _check_reputation(self, phone_number: str) -> Dict:
        """فحص سمعة الرقم"""
        # قاعدة بيانات محلية للتحقق (يمكن تحميلها من ملف)
        spam_database = [
            "+1234567890",
            "+1987654321"
        ]
        
        scam_reports = [
            "+1122334455"
        ]
        
        return {
            'spam_reports': 1 if phone_number in spam_database else 0,
            'scam_reports': 1 if phone_number in scam_reports else 0,
            'trust_score': 85 if phone_number not in spam_database + scam_reports else 30,
            'notes': 'بناءً على قاعدة بيانات محلية'
        }
    
    def _identify_possible_services(self, phone_number: str) -> List[str]:
        """تحديد الخدمات المحتملة المرتبطة بالرقم"""
        services = []
        clean_number = re.sub(r'[^\d]', '', phone_number)
        
        # أنماط للخدمات الشائعة
        patterns = {
            'whatsapp': len(clean_number) >= 10,
            'telegram': len(clean_number) >= 9,
            'signal': len(clean_number) >= 10,
            'banking': any(code in phone_number for code in ['+1', '+44', '+49']),
            'government': len(clean_number) in [10, 11]
        }
        
        for service, condition in patterns.items():
            if condition:
                services.append(service)
        
        return services
    
    def _calculate_privacy_score(self, phone_number: str) -> int:
        """حساب درجة الخصوصية"""
        score = 100
        
        # خصم النقاط بناءً على عوامل الخطر
        if len(phone_number) < 10:
            score -= 20
        
        if phone_number.startswith('+1'):  # أمريكا الشمالية
            score -= 10
        
        # إضافة نقاط للعوامل الإيجابية
        if len(phone_number) >= 12:
            score += 5
        
        return max(0, min(100, score))
    
    def _load_carrier_database(self) -> Dict:
        """تحميل قاعدة بيانات المشغلين"""
        # يمكن تحميل هذا من ملف JSON
        return {
            'verizon': {'country': 'US', 'reliability': 'high'},
            'att': {'country': 'US', 'reliability': 'high'},
            'vodafone': {'country': 'UK', 'reliability': 'high'}
        }
    
    def _load_country_codes(self) -> Dict:
        """تحميل رموز الدول"""
        return {
            '1': 'United States/Canada',
            '44': 'United Kingdom',
            '49': 'Germany',
            '966': 'Saudi Arabia',
            '971': 'UAE',
            '964': 'Iraq'
        }
