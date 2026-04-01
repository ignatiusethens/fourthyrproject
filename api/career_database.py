# Database of foundational Kenyan career clusters mapped to psychological/academic weights

CAREERS = [
    # ---- HEALTH SCIENCES ----
    {
        "name": "Bachelor of Medicine & Surgery (MBChB)",
        "level": "Degree",
        "min_grade": 10.0, # B+ minimum roughly needed
        "subjects": ["biology_grade", "chemistry_grade", "math_grade"],
        "traits": {
            "Laboratory": 10, "Helping": 5, "Research": 5,
            "Team": 3, "Passion": 5, "Wealth": 3, "Outdoors": -5
        }
    },
    {
        "name": "BSc. in Nursing / Public Health",
        "level": "Degree",
        "min_grade": 8.0, 
        "subjects": ["biology_grade", "chemistry_grade"],
        "traits": {
            "Laboratory": 5, "Helping": 10, "Team": 5, "Volunteering": 5, "Passion": 5
        }
    },
    {
        "name": "Diploma in Clinical Medicine / Pharmacy Tech",
        "level": "Diploma",
        "min_grade": 5.0,
        "subjects": ["biology_grade", "chemistry_grade"],
        "traits": {
            "Laboratory": 8, "Helping": 8, "Team": 3
        }
    },
    
    # ---- ENGINEERING & TECHNOLOGY ----
    {
        "name": "BSc. Computer Science / Software Eng.",
        "level": "Degree",
        "min_grade": 9.0,
        "subjects": ["math_grade", "physics_grade"],
        "traits": {
            "Office": 5, "Remote": 10, "Independent": 5, "Research": 5, 
            "Coding": 10, "Wealth": 5, "Flexibility": 5
        }
    },
    {
        "name": "BSc. Civil / Structural Engineering",
        "level": "Degree",
        "min_grade": 9.0,
        "subjects": ["math_grade", "physics_grade"],
        "traits": {
            "Outdoors": 8, "Mechanical": 8, "Building": 10, "Team": 4, "Leading": 4
        }
    },
    {
        "name": "Diploma in Information Technology",
        "level": "Diploma",
        "min_grade": 5.0,
        "subjects": ["math_grade", "english_grade"],
        "traits": {
            "Office": 5, "Remote": 8, "Independent": 5, "Coding": 10
        }
    },
    
    # ---- BUSINESS & ECONOMICS ----
    {
        "name": "Bachelor of Commerce / Economics",
        "level": "Degree",
        "min_grade": 8.0,
        "subjects": ["math_grade", "english_grade"],
        "traits": {
            "Office": 8, "Leading": 5, "Talk": 5, "Trading": 10, 
            "Wealth": 8, "Team": 3
        }
    },
    {
        "name": "Diploma in Business Management",
        "level": "Diploma",
        "min_grade": 5.0,
        "subjects": ["math_grade", "english_grade"],
        "traits": {
            "Office": 6, "Trading": 8, "Talk": 5, "Leading": 3
        }
    },
    
    # ---- ARTS, MEDIA & LAW ----
    {
        "name": "Bachelor of Laws (LLB)",
        "level": "Degree",
        "min_grade": 9.0,
        "subjects": ["english_grade", "kiswahili_grade", "humanities_grade"],
        "traits": {
            "Office": 5, "Talk": 10, "Research": 8, "Independent": 5, 
            "Security": 5, "Wealth": 5
        }
    },
    {
        "name": "BA. in Mass Communication / Journalism",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["english_grade", "kiswahili_grade", "humanities_grade"],
        "traits": {
            "Travel": 8, "Outdoors": 4, "Talk": 8, "Content": 10, "Team": 5
        }
    },
    {
        "name": "BA. in Graphic Design / Fine Arts",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["english_grade", "humanities_grade"],
        "traits": {
            "Remote": 8, "Independent": 8, "Creative": 10, "Content": 10, "Passion": 5
        }
    },
    
    # ---- AGRICULTURE & ENVIRONMENT ----
    {
        "name": "BSc. in Agriculture / Agribusiness",
        "level": "Degree",
        "min_grade": 8.0,
        "subjects": ["biology_grade", "chemistry_grade"],
        "traits": {
            "Outdoors": 10, "Trading": 5, "Mechanical": 3, "Building": 3
        }
    },
    {
        "name": "BSc. Wildlife Management & Conservation",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["biology_grade", "humanities_grade"],
        "traits": {
            "Outdoors": 10, "Travel": 8, "Volunteering": 5, "Passion": 8, "Office": -10
        }
    },
    
    # ---- EDUCATION & SOCIAL SCIENCES ----
    {
        "name": "Bachelor of Education (Arts/Science)",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["english_grade", "kiswahili_grade"],
        "traits": {
            "Helping": 10, "Talk": 8, "Volunteering": 5, "Security": 8, "Passion": 5
        }
    },
    {
        "name": "BA. Social Work / Community Development",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["humanities_grade", "english_grade"],
        "traits": {
            "Helping": 10, "Volunteering": 10, "Travel": 5, "Outdoors": 4, "Passion": 8
        }
    },
    {
        "name": "Diploma in Social Work",
        "level": "Diploma",
        "min_grade": 5.0,
        "subjects": ["humanities_grade", "english_grade"],
        "traits": {
            "Helping": 10, "Volunteering": 10, "Passion": 8
        }
    },
    
    # ---- HOSPITALITY & TOURISM ----
    {
        "name": "BSc. Travel & Tourism Management",
        "level": "Degree",
        "min_grade": 7.0,
        "subjects": ["english_grade", "humanities_grade"],
        "traits": {
            "Travel": 10, "Outdoors": 5, "Talk": 8, "Team": 5, "Flexibility": 5
        }
    },
    {
        "name": "Diploma in Catering & Hotel Management",
        "level": "Diploma",
        "min_grade": 5.0,
        "subjects": ["english_grade"],
        "traits": {
            "Team": 8, "Talk": 5, "Creative": 5, "Building": 3
        }
    },
    
    # ---- ARTISAN / CRAFT CERTIFICATES (Very high demand, lower entry points) ----
    {
        "name": "Artisan in Plumbing & Pipe Fitting",
        "level": "Certificate",
        "min_grade": 0.0, # E or D-
        "subjects": ["math_grade", "physics_grade"],
        "traits": {
            "Outdoors": 8, "Mechanical": 10, "Building": 10, "Independent": 5
        }
    },
    {
        "name": "Artisan in Electrical Installation",
        "level": "Certificate",
        "min_grade": 0.0,
        "subjects": ["math_grade", "physics_grade"],
        "traits": {
            "Outdoors": 5, "Mechanical": 10, "Building": 8, "Security": 8
        }
    },
    {
        "name": "Certificate in Hairdressing & Beauty Therapy",
        "level": "Certificate",
        "min_grade": 0.0,
        "subjects": [],
        "traits": {
            "Creative": 8, "Talk": 8, "Trading": 5, "Independent": 5
        }
    },
    {
        "name": "Certificate in Motor Vehicle Mechanics",
        "level": "Certificate",
        "min_grade": 0.0,
        "subjects": ["physics_grade", "math_grade"],
        "traits": {
            "Mechanical": 10, "Building": 8, "Independent": 5
        }
    }
]
