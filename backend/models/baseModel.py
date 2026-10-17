from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class ReligionModel(BaseModel):
	id: list[int]

class LanguageModel(BaseModel):
	id: list[int]

class RolesModel(BaseModel):
	id: list[int]
	
class UserModel(BaseModel):
	email: EmailStr
	id: int = None
	password: str = None
	otp: str = None
	
class UserInfoModel(BaseModel):
	first_name:     str     | None
	last_name:      str     | None
	screen_name:    str     | None
	phone:          str     | None
	birth_month:    int     | None
	birth_year:     int     | None
	gender:         str     | None
	height:         float| None
	weight:         int     | None

class AddressModel(BaseModel):
	street:     str | None = None
	city:       str | None
	county:     str | None = None
	state:      str | None = None
	zip_code:   str | None = None
	country:    str | None
	from_month: int | None
	from_year:  int | None

class EducationModel(BaseModel):
	completed_year: int | None
	degree:         str | None
	major:          str | None = None
	institution:    str | None
	city:           str | None = None
	state:          str | None = None
	country:        str | None = None

class RelativesModel(BaseModel):
	relation_id:         int | None
	relation_name:       str | None
	relative_name:       str | None
	relative_email: EmailStr | None = None
	relative_phone:      str | None = None
	relative_age:        int | None = None
	relative_location:   str | None = None
	relative_occupation: str | None = None

class WorkHistoryModel(BaseModel):
	work_year:      int | None
	designation:    str | None
	company_name:   str | None
	city:           str | None
	state:          str | None
	country:        str | None

class ConnectionModel(BaseModel):
	email: 			EmailStr | None
	phone: 				 str | None = None
	name:  				 str | None = None
	details: 			 str | None = None
	is_verified: 		 bool| None = False


# data routers
class CandidatesDataPage(BaseModel):
	offset: int = 0
	limit:  int = 10
	gender: str = 'All'