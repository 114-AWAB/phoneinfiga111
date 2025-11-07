import aiohttp
import hashlib
import asyncio
from typing import Dict, List

class BreachScanner:
    def __init__(self):
        self.config = {}
    
    def set_config(self, config: Dict):
        self.config = config
    
    async def comprehensive_check(self, phone_number: str) -> Dict:
        """فحص شامل للتسريبات"""
        tasks = [
            self.check_hibp(phone_number),
            self.check_dehashed(phone_number),
            self.check_breachdirectory(phone_number),
            self.check_local_databases(phone_number)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        breach_results = {
            'count': 0,
            'breaches': [],
            'data_types_found': [],
            'risk_score': 0
        }
        
        for result in results:
            if isinstance(result, dict) and result.get('found', False):
                breach_results['count'] += result.get('count', 0)
                breach_results['breaches'].extend(result.get('breaches', []))
                breach_results['data_types_found'].extend(result.get('data_types', []))
        
        # إزالة التكرارات
        breach_results['data_types_found'] = list(set(breach_results['data_types_found']))
        breach_results['risk_score'] = self._calculate_breach_risk(breach_results)
        
        return breach_results
    
    async def check_hibp(self, phone_number: str) -> Dict:
        """التحقق من Have I Been Pwned"""
        try:
            api_key = self.config.get('hibp_api_key')
            if not api_key:
                return {'found': False, 'error': 'No API key'}
            
            # تحويل الرقم إلى hash
            phone_hash = hashlib.sha1(phone_number.encode()).hexdigest().upper()
            
            async with aiohttp.ClientSession() as session:
                headers = {'hibp-api-key': api_key}
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{phone_number}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        breaches = await response.json()
                        return {
                            'found': True,
                            'count': len(breaches),
                            'breaches': breaches,
                            'data_types': self._extract_data_types(breaches),
                            'source': 'Have I Been Pwned'
                        }
                    else:
                        return {'found': False}
        
        except Exception as e:
            return {'found': False, 'error': str(e)}
    
    async def darkweb_scan(self, phone_number: str) -> Dict:
        """مسح Dark Web (محاكاة)"""
        # في النسخة الحقيقية، هذا يتطلب وصولاً متخصصاً
        return {
            'found': False,
            'message': 'Dark Web scanning requires specialized access',
            'risk_level': 'unknown'
        }
    
    def _calculate_breach_risk(self, breach_data: Dict) -> int:
        """حساب درجة خطورة التسريبات"""
        risk_score = 0
        
        # عدد التسريبات
        risk_score += min(breach_data['count'] * 10, 50)
        
        # أنواع البيانات المسربة
        sensitive_data = ['passwords', 'credit_cards', 'ssn', 'banking']
        data_types = breach_data['data_types_found']
        
        for data_type in data_types:
            if any(sensitive in data_type.lower() for sensitive in sensitive_data):
                risk_score += 20
        
        return min(risk_score, 100)
    
    def _extract_data_types(self, breaches: List) -> List[str]:
        """استخراج أنواع البيانات من التسريبات"""
        data_types = []
        for breach in breaches:
            if 'DataClasses' in breach:
                data_types.extend(breach['DataClasses'])
        return list(set(data_types))
