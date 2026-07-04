from django.core.management.base import BaseCommand
from courses.models import User, Category, Course, Section, Lesson, Enrollment, Progress

class Command(BaseCommand):
    help = 'Mengisi database dengan data awal yang lengkap untuk keperluan testing API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Memulai proses seeding data lengkap...')

        # 1. Buat User Instructor
        instructor, _ = User.objects.get_or_create(
            username='dosen_teladan',
            defaults={'role': 'instructor', 'email': 'dosen@udinus.ac.id'}
        )
        instructor.set_password('InstructorLMS2026!')
        instructor.save()

        # 2. Buat User Student
        student, _ = User.objects.get_or_create(
            username='student_demo',
            defaults={'role': 'student', 'email': 'student@udinus.ac.id'}
        )
        student.set_password('StudentLMS2026!')
        student.save()

        # 3. Buat Kategori
        category, _ = Category.objects.get_or_create(
            name='Backend Development',
            defaults={'description': 'Kategori khusus materi pemrograman sisi server.'}
        )

        # 4. Buat Course
        course, _ = Course.objects.get_or_create(
            title='Mastering Django Ninja',
            defaults={'description': 'Belajar membangun REST API dengan cepat.', 'category': category, 'instructor': instructor}
        )

        # 5. Buat Section (Modul)
        section, _ = Section.objects.get_or_create(
            course=course,
            title='Pengenalan Framework',
            defaults={'order': 1}
        )

        # 6. Buat Lesson (Materi)
        lesson1, _ = Lesson.objects.get_or_create(
            course=course,
            section=section,
            title='Instalasi Django Ninja',
            defaults={'content': 'Langkah-langkah instalasi pip install django-ninja...', 'order': 1}
        )
        
        lesson2, _ = Lesson.objects.get_or_create(
            course=course,
            section=section,
            title='Membuat Endpoint Pertama',
            defaults={'content': 'Cara menggunakan router.get...', 'order': 2}
        )

        # 7. Daftarkan Student ke Course (Enrollment)
        Enrollment.objects.get_or_create(student=student, course=course)

        # 8. Tandai Progress (Student menyelesaikan Lesson 1)
        Progress.objects.get_or_create(
            student=student, 
            lesson=lesson1, 
            defaults={'is_completed': True}
        )

        self.stdout.write(self.style.SUCCESS(f'SEEDING LENGKAP SELESAI!'))
        self.stdout.write(self.style.SUCCESS(f'- Course ID: {course.id}'))
        self.stdout.write(self.style.SUCCESS(f'- Student di-enroll ke Course tersebut.'))
        self.stdout.write(self.style.SUCCESS(f'- Student menyelesaikan 1 dari 2 lesson (Progress 50%).'))