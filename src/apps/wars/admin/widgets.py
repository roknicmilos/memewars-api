from django.contrib.admin.widgets import AdminFileWidget


class MemeImageAdminWidget(AdminFileWidget):
    template_name = 'clearable_file_input.html'
