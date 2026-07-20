from pydantic import BaseModel, EmailStr, HttpUrl


class TeamMember(BaseModel):
    name: str

    role: str

    photo_filename: str

    email: EmailStr

    github: HttpUrl | None = None

    linkedin: HttpUrl | None = None

    portfolio: HttpUrl | None = None

    contributions: list[str]


TEAM_MEMBERS: list[TeamMember] = [

    TeamMember(

        name="Mudit Dua",

        role="Lead Backend & Frontend Development",

        photo_filename="mudit.webp",

        email="reachmuditdua@gmail.com",

        github="https://github.com/muditdua",

        linkedin="https://www.linkedin.com/in/mudit-dua-2a30a1223/",

        contributions=[

        "Designed the FastAPI backend architecture",

        "Developed the core frontend and backend application",

        "Integrated Gemini AI and implemented streaming responses (SSE)",

        "Assisted with Docker containerization"

    ]

    ),

    TeamMember(

        name="Ananya Singh Chauhan",

        role="Co-Lead Frontend and Backend Development",

        photo_filename="ananya.webp",

        email="ananya.chauhan1306@gmail.com",

        github="https://github.com/ananya130606",

        linkedin="https://www.linkedin.com/in/ananyasinghchauhan/",

        contributions=[

        "Built the initial project prototype and application foundation",

        "Co-developed the frontend interface and assisted in backend implementation",

        "Prepared the project concept note",

        "Managed Docker deployment and AWS cloud deployment"

    ]

    ),

    TeamMember(

        name="Ramya Gupta",

        role="Team Leader",

        photo_filename="ramya3.webp",

        email="ramyagupta7172@gmail.com",

        linkedin="https://www.linkedin.com/in/ramya-gupta-353526273/",

        contributions=[

        "Coordinated team communication and task allocation",

        "Managed project planning and submission activities"
        ]

    ),
    TeamMember(

        name="Vidhi Kapoor",

        role="Project Member",

        photo_filename="vidhi.webp",

        email="kapoorvidhi6@gmail.com",

        linkedin="https://www.linkedin.com/in/vidhi-kapoor-39b6aa276/",

        contributions=[

            "Co-authored the final project report",

            "Assisted with project documentation"

        ]

    ),
    TeamMember(
        name="Yogus Wadhwa",

        role="N/A",

        photo_filename="yogus3.webp",

        email="yoguswadhwa@gmail.com",

        linkedin="https://www.linkedin.com/in/yogus-wadhwa-41b4042b0/",

        contributions=[

            "⚠ Error retrieving contribution data."

        ]

    ),
    TeamMember(

        name="Prateek",

        role="Project Member",

        photo_filename="prateek.webp",

        email="Parteek562006@gmail.com",

        linkedin="https://www.linkedin.com/in/parteek-745a7037a/",

        contributions=[

            "Co-authored the final project report",
            "Prepared project documentation for submission"

        ]

    ),

]