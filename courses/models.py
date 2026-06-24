from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField("nama matkul", max_length=100)
    description = models.TextField("deskripsi", default='-')
    price = models.IntegerField("harga", default=10000)
    image = models.ImageField("gambar", null=True, blank=True)
    enrollment_count = models.PositiveIntegerField(default=0)
    completion_count = models.PositiveIntegerField(default=0)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="pengajar",
        on_delete=models.RESTRICT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"
        indexes = [
            models.Index(fields=['name'], name='idx_course_name'),
        ]

ROLE_OPTIONS = [
    ('std', "Siswa"),
    ('ast', "Asisten"),
]

class CourseMember(models.Model):
    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="siswa",
        on_delete=models.RESTRICT
    )
    roles = models.CharField(
        "peran",
        max_length=3,
        choices=ROLE_OPTIONS,
        default='std'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    certificate_path = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user_id} - {self.course_id} ({self.roles})"

    @property
    def is_completed(self):
        return self.completed_at is not None

    class Meta:
        verbose_name = "Anggota Kelas"
        verbose_name_plural = "Anggota Kelas"
        constraints = [
            models.UniqueConstraint(
                fields=['course_id', 'user_id'],
                name='unique_course_member'
            )
        ]

class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField(
        'URL Video',
        max_length=200,
        null=True,
        blank=True
    )
    file_attachment = models.FileField("File", null=True, blank=True)
    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )
    parent_id = models.ForeignKey(
        "self",
        verbose_name="induk",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Konten Kelas"
        verbose_name_plural = "Konten Kelas"

class Comment(models.Model):
    content_id = models.ForeignKey(
        CourseContent,
        verbose_name="konten",
        on_delete=models.CASCADE
    )
    member_id = models.ForeignKey(
        CourseMember,
        verbose_name="pengguna",
        on_delete=models.CASCADE
    )
    comment = models.TextField('komentar')

    def __str__(self):
        return f"Komentar oleh {self.member_id} pada {self.content_id}"

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"
