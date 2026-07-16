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

        role="Lead Frontend & Backend Development",

        photo_filename="mudit.webp",

        email="reachmuditdua@gmail.com",

        github="https://github.com/muditdua",

        linkedin="https://www.linkedin.com/in/mudit-dua-2a30a1223/",

        contributions=[

            "Designed FastAPI backend",

            "Integrated Gemini AI",

            "Developed ATS Resume Analyzer",

            "Designed project architecture",

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

            "Designed dashboard UI",

            "Built responsive layouts",

            "Implemented animations",

            "Improved accessibility"

        ]

    ),

    TeamMember(

        name="Ramya Gupta",

        role="Team Leader - Reports",

        photo_filename="ramya3.webp",

        email="ramyagupta7172@gmail.com",

        linkedin="https://www.linkedin.com/in/ramya-gupta-353526273/",

        contributions=[

            "Lead the team",

            "Managing roles",

            "Setup AWS",

        ]

    ),
    TeamMember(

        name="Vidhi Kapoor",

        role="Reports and Documentation",

        photo_filename="vidhi.webp",

        email="kapoorvidhi6@gmail.com",

        linkedin="https://www.linkedin.com/in/vidhi-kapoor-39b6aa276/",

        contributions=[

            "PRD Documentation",

            "Built responsive layouts",

            "Implemented animations",

            "Improved accessibility"

        ]

    ),
    TeamMember(

        name="Yogus Wadhwa",

        role="Vella behta rha kuch nahi kara mein project ka naam bhi ni pata",

        photo_filename="yogus2.webp",

        email="yoguswadhwa@gmail.com",

        linkedin="https://www.linkedin.com/in/yogus-wadhwa-41b4042b0/",

        contributions=[

            "Nothing"

        ]

    ),
    TeamMember(

        name="Prateek",

        role="Paperwork and AWS",

        photo_filename="prateek.webp",

        email="Parteek562006@gmail.com",

        linkedin="https://www.linkedin.com/in/parteek-745a7037a/",

        contributions=[

            "Designed dashboard UI",

            "Built responsive layouts",

            "Implemented animations",

            "Improved accessibility"

        ]

    ),

]