import logging
from datetime import date
from typing import List, Dict, Optional, Any

from .rest_adapter import Rest
from .utils import create_payload, create_metadata_payload, create_company_info, create_fixed_info
from .models import Applicant, Document


class SumSubAPI:
    def __init__(self, secret_key, app_token: str, base_url: str = 'https://api.sumsub.com', ver: str = 'v1',
                 ssl_verify: bool = True,
                 logger: logging.Logger = None):
        self.rest = Rest(base_url=base_url, secret_key=secret_key, app_token=app_token)

    def create_applicant(self, level_name: str, external_user_id: str, company_name: str, registration_number: str, company_country: str,
                         legal_address: str, company_address: Dict[str, str], incorporated_on: str, company_type: str,
                         company_email: str, company_phone: str, control_scheme: str, tax_id: str,
                         registration_location: str, website: str, postal_address: str,
                         beneficiaries: List[Dict[str, Any]], no_ubos: bool, no_shareholders: bool, source_key: str,
                         applicant_email: str, applicant_phone: str, lang: str, first_name: str, middle_name: str,
                         last_name: str, legal_name: str, gender: str, dob: str, place_of_birth: str,
                         country_of_birth: str, state_of_birth: str, country: str, nationality: str,
                         addresses: List[Dict[str, str]], tin: str, applicant_type: str = "company"):
        company_info = create_company_info(
            company_name=company_name, registration_number=registration_number, country=company_country,
            legal_address=legal_address,address=company_address, incorporated_on=incorporated_on, type=company_type,
            email=company_email, phone=company_phone, control_scheme=control_scheme, tax_id=tax_id,
            registration_location=registration_location, website=website, postal_address=postal_address,
            beneficiaries=beneficiaries, no_ubos=no_ubos, no_shareholders=no_shareholders)

        fixed_info = create_fixed_info(
            first_name=first_name, middle_name=middle_name, last_name=last_name, legal_name=legal_name, gender=gender,
            dob=dob, place_of_birth=place_of_birth, country_of_birth=country_of_birth, state_of_birth=state_of_birth,
            country=country, nationality=nationality, addresses=addresses, tin=tin)

        payload = create_payload(
            external_user_id=external_user_id, info={"companyInfo": company_info}, source_key=source_key,
            email=applicant_email, phone=applicant_phone, lang=lang, fixed_info=fixed_info, type=applicant_type)

        response = self.rest.post(endpoint=f'/resources/applicants?levelName={level_name}',
                                  params={'levelName': level_name}, data=payload)
        return Applicant(**response.data)

    def add_id_document(self, applicant_id: str, id_doc_type: str, id_doc_sub_type: str, country: str, first_name: str,
                        last_name: str, number: str, content: str, middle_name: Optional[str] = None,
                        issued_date: Optional[date] = None, valid_until: Optional[date] = None,
                        dob: Optional[date] = None, place_of_birth: Optional[str] = None):
        payload = create_metadata_payload(
            id_doc_type=id_doc_type, id_doc_sub_type=id_doc_sub_type, country=country, first_name=first_name,
            last_name=last_name, number=number, content=content, middle_name=middle_name, issued_date=issued_date,
            valid_until=valid_until, dob=dob, place_of_birth=place_of_birth)

        response = self.rest.post(endpoint=f'/resources/applicants/{applicant_id}/info/idDoc', data=payload)
        return Document(**response.data)

    def get_verification_status(self, applicant_id: str):
        response = self.rest.get(endpoint=f'/resources/applicants/{applicant_id}/one')
        return Applicant(**response.data)
