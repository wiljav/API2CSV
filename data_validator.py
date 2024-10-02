from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict

class Drink(BaseModel):
    idDrink: int
    strDrink: str
    strCategory: Optional[str]
    strAlcoholic: Optional[str]
    strInstructions: Optional[str]
    strIngredient1: Optional[str]

# class APIResponse(BaseModel):
#     drinks: List[Drink]
def validate_data(all_data: List[Dict]) -> None:
    valid_count = 0
    invalid_count = 0
    invalid_records = []

    for record in all_data:
        try:
            Drink(**record)
            valid_count += 1
        except ValidationError as e:
            invalid_count += 1
            invalid_records.append(record)

    # Printing summary
    total_count = valid_count + invalid_count
    print(f"Total records processed: {total_count}")
    print(f"Valid records: {valid_count}")
    print(f"Invalid records: {invalid_count}")

    # Printing invalid records
    if invalid_records:
        print("Invalid records:", invalid_records)
    return valid_count, invalid_count