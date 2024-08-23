from datetime import date
from typing import List, Dict, Optional, Any


def create_payload(external_user_id: str, info: Dict[str, Dict], source_key: str, email: str, phone: str, lang: str,
                   fixed_info: Dict[str, Any], type: str) -> Dict[str, Any]:
    """
    Create a payload dictionary based on the provided arguments.

    :param external_user_id: External user ID
    :param info: Dictionary containing company information
    :param source_key: Source key
    :param email: Email address
    :param phone: Phone number
    :param lang: Language code
    :param fixed_info: Dictionary containing fixed information
    :param type: Type of entity (e.g., 'company')
    :return: A dictionary representing the payload
    """
    return {"externalUserId": external_user_id, "info": info, "sourceKey": source_key, "email": email, "phone": phone,
            "lang": lang, "fixedInfo": fixed_info, "type": type}


def create_company_info(company_name: str, registration_number: str, country: str, legal_address: str,
                        address: Dict[str, str], incorporated_on: str, type: str, email: str, phone: str,
                        control_scheme: str, tax_id: str, registration_location: str, website: str, postal_address: str,
                        beneficiaries: List[Dict[str, Any]], no_ubos: bool, no_shareholders: bool) -> Dict[str, Any]:
    """
    Create a company info dictionary based on the provided arguments.

    :param company_name: Name of the company
    :param registration_number: Company registration number
    :param country: Country of registration
    :param legal_address: Legal address of the company
    :param address: Dictionary containing address details
    :param incorporated_on: Date of incorporation
    :param type: Type of company
    :param email: Company email address
    :param phone: Company phone number
    :param control_scheme: Control scheme of the company
    :param tax_id: Tax ID of the company
    :param registration_location: Location of registration
    :param website: Company website
    :param postal_address: Postal address of the company
    :param beneficiaries: List of dictionaries containing beneficiary information
    :param no_ubos: Boolean indicating if there are no Ultimate Beneficial Owners
    :param no_shareholders: Boolean indicating if there are no shareholders
    :return: A dictionary representing the company info
    """
    return {"companyName": company_name, "registrationNumber": registration_number, "country": country,
            "legalAddress": legal_address, "address": address, "incorporatedOn": incorporated_on, "type": type,
            "email": email, "phone": phone, "controlScheme": control_scheme, "taxId": tax_id,
            "registrationLocation": registration_location, "website": website, "postalAddress": postal_address,
            "beneficiaries": beneficiaries, "noUBOs": no_ubos, "noShareholders": no_shareholders}


def create_fixed_info(first_name: str, middle_name: str, last_name: str, legal_name: str, gender: str, dob: str,
                      place_of_birth: str, country_of_birth: str, state_of_birth: str, country: str, nationality: str,
                      addresses: List[Dict[str, str]], tin: str) -> Dict[str, Any]:
    """
    Create a fixed info dictionary based on the provided arguments.

    :param first_name: First name
    :param middle_name: Middle name
    :param last_name: Last name
    :param legal_name: Legal name
    :param gender: Gender ('M' or 'F')
    :param dob: Date of birth
    :param place_of_birth: Place of birth
    :param country_of_birth: Country of birth
    :param state_of_birth: State of birth
    :param country: Country
    :param nationality: Nationality
    :param addresses: List of dictionaries containing address information
    :param tin: Tax Identification Number
    :return: A dictionary representing the fixed info
    """
    return {"firstName": first_name, "middleName": middle_name, "lastName": last_name, "legalName": legal_name,
            "gender": gender, "dob": dob, "placeOfBirth": place_of_birth, "countryOfBirth": country_of_birth,
            "stateOfBirth": state_of_birth, "country": country, "nationality": nationality, "addresses": addresses,
            "tin": tin}


def create_metadata_payload(id_doc_type: str, id_doc_sub_type: str, country: str, first_name: str, last_name: str,
                            number: str, content: str, middle_name: Optional[str] = None,
                            issued_date: Optional[date] = None, valid_until: Optional[date] = None,
                            dob: Optional[date] = None, place_of_birth: Optional[str] = None) -> dict:
    """
    Create a payload dictionary based on the provided arguments.

    :param id_doc_type: Type of ID document
    :param id_doc_sub_type: Subtype of ID document
    :param country: Country of the document
    :param first_name: First name of the document holder
    :param last_name: Last name of the document holder
    :param number: Document number
    :param content: Content string
    :param middle_name: Middle name of the document holder (optional)
    :param issued_date: Date the document was issued (optional)
    :param valid_until: Date until which the document is valid (optional)
    :param dob: Date of birth of the document holder (optional)
    :param place_of_birth: Place of birth of the document holder (optional)
    :return: A dictionary representing the payload
    """
    metadata = {"idDocType": id_doc_type, "idDocSubType": id_doc_sub_type, "country": country, "firstName": first_name,
                "lastName": last_name, "number": number}

    # Add optional fields if they are provided
    if middle_name:
        metadata["middleName"] = middle_name
    if issued_date:
        metadata["issuedDate"] = issued_date.isoformat()
    if valid_until:
        metadata["validUntil"] = valid_until.isoformat()
    if dob:
        metadata["dob"] = dob.isoformat()
    if place_of_birth:
        metadata["placeOfBirth"] = place_of_birth

    return {
        "metadata": metadata,
        "content": content
    }
