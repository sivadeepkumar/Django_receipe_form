from django.contrib import admin
from home.models import *
from product.models import *
from django.db.models import Sum 


admin.site.register(Receipe)
admin.site.register(Student)
admin.site.register(StudentID)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SubjectMarks)
admin.site.register(NoticeBoard)




class ReportCardAdmin(admin.ModelAdmin):
    list_display=['student','student_rank','total_marks','date_of_report_card_generation']

    def total_marks(self,obj):
        subject_marks = SubjectMarks.objects.filter(student = obj.student)
        print(subject_marks.aggregate(marks = Sum('marks')))
        
        return 0

admin.site.register(ReportCard,ReportCardAdmin)


class ShowAttributes(admin.ModelAdmin):
    list_display = ['student','subject','marks']


