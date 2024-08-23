from datetime import date, datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class IdDoc:
    idDocType: str
    country: str
    firstName: str
    firstNameEn: str
    lastName: str
    lastNameEn: str
    validUntil: str
    number: str
    dob: str
    mrzLine1: str
    mrzLine2: str
    mrzLine3: str


@dataclass
class FixedInfo:
    firstName: str
    lastName: str


@dataclass
class Info:
    firstName: str
    firstNameEn: str
    lastName: str
    lastNameEn: str
    dob: str
    country: str
    idDocs: List[IdDoc]


@dataclass
class Agreement:
    createdAt: str
    source: str
    targets: List[str]


@dataclass
class DocSet:
    idDocSetType: str
    types: List[str]


@dataclass
class RequiredIdDocs:
    docSets: List[DocSet]


@dataclass
class ReviewResult:
    reviewAnswer: str


@dataclass
class Review:
    elapsedSincePendingMs: int
    elapsedSinceQueuedMs: int
    reprocessing: bool
    levelName: str
    createDate: str
    reviewDate: str
    reviewResult: ReviewResult
    reviewStatus: str


@dataclass
class Applicant:
    id: str
    createdAt: str
    clientId: str
    inspectionId: str
    externalUserId: str
    fixedInfo: FixedInfo
    info: Info
    agreement: Agreement
    email: str
    applicantPlatform: str
    requiredIdDocs: RequiredIdDocs
    review: Review
    lang: str
    type: str


@dataclass
class Document:
    idDocType: str
    country: str
    issuedDate: date
    number: str
    dob: date
    placeOfBirth: str


@dataclass
class Response:
    status_code: int
    data: Dict



