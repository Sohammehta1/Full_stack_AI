class outOfIngredientsError(Exception):
    pass

def makeChai(milk,sugar):
    try:
        if milk == 0 or sugar==0:
            raise outOfIngredientsError("Missing milk or sugar")
        print("chai is ready")
    except outOfIngredientsError as e:
        print(e)

    


makeChai(0,0)