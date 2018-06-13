_API_V1_PREFIX = '/api/v1'
_YOGA_PREFIX = '/yoga'

# Data routes
TEACHERS_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/teachers'
TEACHER_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/teacher/<string:username>'
STUDENTS_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/students'
STUDENT_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/student/<string:username>'
ABONEMENTS_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/abonements'
ABONEMENT_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/abonement/<string:name>'
LESSONS_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/lessons'
LESSON_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/lesson/<string:name>'
LESSONATTENDANCELIST_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/lessonattendances'
LESSONATTENDANCE_URL = _API_V1_PREFIX + _YOGA_PREFIX + '/lessonattendance/<string:lessonid>'




# Data routes store
STORE_URL = '/store/<string:name>'
STORE_LIST_URL = '/stores'
ITEMS_URL = '/items'
ITEM_URL = '/item/<string:name>'
USER_REGISTER_URL = '/register'


STRING_FAIL = 'fail'
STRING_SUCCESS = 'success'