import datetime


#in case there is no reference number retrieved from the database, the function takes the department selected by the user as an argument
def generate_first_reference_number(selected_department):
    date_today = datetime.datetime.now()
    day_today = date_today.strftime("%d")
    current_month = date_today.strftime("%m")
    year_of = date_today.strftime("%G")
    department = selected_department # to be replaced with select statement
    initial_int = 0
    initial_int += 1
    initial_id = str(initial_int)
    initial_ref_no = f"REF/{year_of}/{current_month}/{day_today}/{department}/{initial_id}"
    return (initial_ref_no)
    #print(initial_ref_no)
    

#the function takes the reference number from the database as the first argument and the departemnet chosen by the user as the second argument
def generate_new_reference_number(mydb_result,selected_department):
    """accessing the first tuple item in mydb_result var(the reference number)
    when you fetch the last reference number entered, the result is returned as a tuple
    so to access the reference number in the tuple you just access the first item in the 
    tuple."""
    string_result= mydb_result[0]
    """stripping off the rest of the reference number(obtaining the part with the unique id). The reference number
    generated has string length of 20 characters which is goig to change depending on the length of the unique id.
    To obtain the unique id you fetch the string characters that come after the 19th character which will be the
    forward-slash separating the department initials and the unique id(REF/2021/08/23/ICT/2)"""
    create_list_from_result= string_result.split('/')
    id_index= create_list_from_result.__len__()
    string_unique_id= create_list_from_result[id_index-1]
    date_today = datetime.datetime.now()
    day_today = date_today.strftime("%d")
    current_month = date_today.strftime("%m")
    year_of = date_today.strftime("%G")
    department = selected_department  # to be replaced with select statement
    #generating the new reference number
    stripped_id_integer = int(string_unique_id)
    stripped_id_integer += 1
    new_id = str(stripped_id_integer)
    new_ref_no = f"REF/{year_of}/{current_month}/{day_today}/{department}/{new_id}"
    return (new_ref_no)
    #print(new_ref_no)


