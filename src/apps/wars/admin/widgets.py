from django.contrib.admin.widgets import AdminFileWidget


class MemeAdminWidget(AdminFileWidget):
    template_name = 'clearable_file_input.html'
