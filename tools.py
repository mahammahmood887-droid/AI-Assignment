import os


GRADE_BANDS = [
    (85, 100, "A", 4.0),
    (80, 84, "A-", 3.7),
    (75, 79, "B+", 3.3),
    (70, 74, "B", 3.0),
    (65, 69, "B-", 2.7),
    (61, 64, "C+", 2.3),
    (58, 60, "C", 2.0),
    (55, 57, "C-", 1.7),
    (50, 54, "D", 1.0),
    (0, 49, "F", 0.0),
]


COURSES = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5),
    ],
}


MD_COURSES = {"MD-001", "MD-002"}


def marks_to_grade_points(marks: int) -> float | str:
    """Convert marks from 0-100 into the PUCIT grade point.

    Use this whenever the student gives marks instead of a grade or
    grade point (e.g. "I got 78 in AI"). Call it once per course, then
    feed the resulting grade points into calculate_semester_gpa. Do not
    work out the grade point yourself.
    """
    if not isinstance(marks, int) or isinstance(marks, bool):
        return "Error: marks must be a whole number"

    if marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"

    for low, high, _grade, points in GRADE_BANDS:
        if low <= marks <= high:
            return points

    return "Error: could not determine a grade for the given marks"


def calculate_semester_gpa(
    grade_points: list[float],
    credit_hours: list[float],
) -> float | str:
    """Calculate the credit-weighted GPA for one semester.

    Use this once you have a grade point for every course the student
    took that semester (from marks_to_grade_points, or given directly)
    and the matching credit hours, in the same order. Leave out any
    Math Deficiency courses (MD-001, MD-002) - they are non-credit
    pass/fail and never count toward GPA. Never average these by hand.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours must not be empty"

    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be the same length"

    total_ch = sum(credit_hours)

    if total_ch <= 0:
        return "Error: total credit hours must be greater than zero"

    weighted_total = sum(
        grade_point * credit_hour
        for grade_point, credit_hour in zip(grade_points, credit_hours)
    )

    return round(weighted_total / total_ch, 2)


def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float | str:
    """Calculate the new CGPA after adding one semester.

    Use this when the student already has a current CGPA and completed
    credit hours, and gives (or asks you to project) a GPA for one more
    semester, and wants to know their overall CGPA afterward. Never
    estimate this yourself.
    """
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"

    if semester_credit_hours <= 0:
        return "Error: semester_credit_hours must be greater than zero"

    if not 0.0 <= current_cgpa <= 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"

    if not 0.0 <= semester_gpa <= 4.0:
        return "Error: semester_gpa must be between 0.0 and 4.0"

    total_hours = completed_credit_hours + semester_credit_hours

    cgpa = (
        current_cgpa * completed_credit_hours
        + semester_gpa * semester_credit_hours
    ) / total_hours

    return round(cgpa, 2)


def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float | str:
    """Calculate the GPA needed over the remaining credit hours to reach
    a target CGPA.

    Use this whenever the student states or implies a target CGPA (e.g.
    "I want to graduate with a 3.5") and you know their current CGPA,
    completed credit hours, and remaining credit hours. This can return
    a value above 4.0, which is impossible - in that case do not report
    it as the answer. Instead call this again with more
    remaining_credit_hours (a longer horizon, using
    get_remaining_credit_hours across more semesters) until the result
    is at or below 4.0, then tell the student which horizon works.
    """
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than zero"

    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"

    if not 0.0 <= target_cgpa <= 4.0:
        return "Error: target_cgpa must be between 0.0 and 4.0"

    if not 0.0 <= current_cgpa <= 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"

    total_hours = completed_credit_hours + remaining_credit_hours

    required = (
        target_cgpa * total_hours
        - current_cgpa * completed_credit_hours
    ) / remaining_credit_hours

    return round(required, 2)


def get_semester_courses(semester: int) -> str:
    """Return the courses and credit hours for a semester.

    Use this when the student needs to know what's in a semester (e.g.
    "what's in semester 5"), or when you need the credit hours for each
    course to build the credit_hours list for calculate_semester_gpa.
    Returns a formatted string - present it as-is or summarize it.
    """
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"

    result = [f"Semester {semester} courses:"]
    total = 0.0

    for code, name, credit_hours in COURSES[semester]:
        result.append(
            f"  {code} - {name} ({credit_hours} credit hours)"
        )
        total += credit_hours

    result.append(
        f"Semester {semester} total: {total} credit hours"
    )

    return "\n".join(result)


def get_remaining_credit_hours(current_semester: int, through_semester: int = 8) -> float | str:
    """Total the graded credit hours in a window of semesters AFTER
    `current_semester`, up to and including `through_semester`.

    Use this to get remaining_credit_hours for required_gpa_for_target.
    Pass current_semester = the student's LAST COMPLETED semester (their
    current semester minus 1; use 0 if they are in semester 1). Leave
    through_semester at 8 for the whole rest of the degree, or lower it to
    test a shorter horizon. Example, student in semester 5 (last completed
    = 4): (4, 5) = semester V only, (4, 6) = V-VI, (4, 7) = V-VII,
    (4, 8) = V-VIII. Never add semester totals yourself.
    """
    if not isinstance(current_semester, int) or isinstance(current_semester, bool):
        return "Error: current_semester must be a whole number"

    if not 0 <= current_semester <= 7:
        return "Error: current_semester must be between 0 and 7"

    if not isinstance(through_semester, int) or isinstance(through_semester, bool):
        return "Error: through_semester must be a whole number"

    if not current_semester < through_semester <= 8:
        return "Error: through_semester must be after current_semester and at most 8"

    total = 0.0
    for semester in range(current_semester + 1, through_semester + 1):
        for _code, _name, credit_hours in COURSES[semester]:
            total += credit_hours

    return total


def save_report(filename: str, content: str) -> str:
    """Save a GPA or CGPA report as a text file.

    Only call this after the student explicitly asks to save, and only
    once you've already produced something worth keeping (a semester
    GPA, a projected CGPA, or a target-GPA plan) with the other tools.
    Never call this after a clarifying question or a single grade
    lookup, and never call it unprompted.
    """
    if not filename or not filename.strip():
        return "Error: filename must not be empty"

    filename = os.path.basename(filename.strip())

    if filename in (".", ".."):
        return "Error: filename must not be empty"

    if not filename.endswith(".txt"):
        filename += ".txt"

    try:
        os.makedirs("reports", exist_ok=True)

        path = os.path.join("reports", filename)

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return f"Report saved as {path}"

    except OSError as error:
        return f"Error: could not save file ({error})"