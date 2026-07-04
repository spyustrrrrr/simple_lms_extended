from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Course, Section, Lesson, Enrollment, Progress, Review, Wishlist

# Tetap gunakan bawaan untuk User
# admin.site.register(User, UserAdmin)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Role Custom', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)

# Kustomisasi tampilan tabel lainnya
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    ordering = ('course', 'order')

# Untuk model sisanya, biarkan standar jika tidak ingin terlalu panjang
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(Wishlist)