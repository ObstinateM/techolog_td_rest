from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    first_name: str
    last_name: str
    ssn: str  # Social Security Number

    @field_validator('first_name', "last_name")
    @classmethod
    def name_must_not_contain_space(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('must not contain a space')
        return v.title()
    
    # # Example value : 102069122233344
    @field_validator('ssn')
    @classmethod
    def ssn_validator(self, v: str) -> str:
        if len(v) != 15:
            raise ValueError('must be 15 digits')
        # Sex check
        if v[0] not in ['1', '2']:
            raise ValueError('must start with 1 or 2')
        # Year check
        if int(v[1:3]) < 0 and int(v[1:3]) > 99:
            raise ValueError('Year must be between 00 and 99')
        # Month check
        if int(v[3:5]) < 1 and int(v[3:5]) > 12:
            raise ValueError('Month must be between 01 and 12')
        # Department check
        if int(v[5:7]) < 1 and int(v[5:7]) > 99:
            raise ValueError('Department must be between 01 and 99')
        # Country check
        if int(v[7:10]) < 1 and int(v[7:10]) > 999:
            raise ValueError('Country must be between 001 and 999')
        # Birth index check
        if int(v[10:13]) < 1 and int(v[10:13]) > 999:
            raise ValueError('Birth index must be between 001 and 999')
        # Control key check
        if int(v[13:15]) < 1 and int(v[13:15]) > 97:
            raise ValueError('Control key must be between 01 and 97')
        return v

    def decrypt(self):
        sex = "Homme" if int(self.ssn[0]) == 1 else "Femme"
        year = self.ssn[1:3]
        month = self.ssn[3:5]
        department = self.ssn[5:7]
        country = self.ssn[7:10]
        birth_index = self.ssn[10:13]
        control_key = self.ssn[13:15]
        return {
            "sex": sex,
            "year": year,
            "month": month,
            "department": department,
            "country": country,
            "birth_index": birth_index,
            "control_key": control_key
        }

class PatientWithOnlyName(BaseModel):
    first_name: str
    last_name: str

    @field_validator('first_name', "last_name")
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('must not contain a space')
        return v.title()