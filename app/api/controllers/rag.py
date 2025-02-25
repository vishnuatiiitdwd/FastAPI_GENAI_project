from app.data.document import identification_file
from app.services.rag_services import generate_role_based_response

def rag_response(filepath,query,file_extension,current_user_role):
    identification_file(filepath)
    return generate_role_based_response(query,current_user_role)




    