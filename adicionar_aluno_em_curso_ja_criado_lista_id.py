import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopos necessários para listar cursos e adicionar alunos no Google Classroom
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.rosters"
]

def main():
    """
    Código usado para poder criar e exibir as salas do Google criadas e adicionar alunos aos cursos.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Vai pedir autenticação 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Salva as credenciais e mostra os cursos
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("classroom", "v1", credentials=creds)

        # Chama a API Do classroom para ver os cursos deixar em 1000
        results = service.courses().list(pageSize=1000).execute()
        courses = results.get("courses", [])

        if not courses:
            print("No courses found.")
            return
        # Mostra na tela o nome dos cursos criados e salas
        print("Courses:")
        for course in courses:
            print(f'{course["name"]} (ID: {course["id"]})')

        # Adicionar aluno ao curso
        course_id = input("Digite o ID do curso para adicionar um aluno: ")
        student_email = input("Digite o e-mail do aluno: ")
        add_student_to_course(service, course_id, student_email)

    except HttpError as error:
        print(f"An error occurred: {error}")

def add_student_to_course(service, course_id, student_email):
    try:
        student = {
            'userId': student_email
        }
        student = service.courses().students().create(courseId=course_id, body=student).execute()
        print(f"Student {student_email} added to course {course_id}")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    # Apagar o arquivo token.json para forçar a reautenticação
    if os.path.exists("token.json"):
        os.remove("token.json")
    main()
