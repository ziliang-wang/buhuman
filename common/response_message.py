
class UserMessage(object):
    # 嚮應狀態碼規定
    # 嚮應給前端的，已1開頭，
    # 成功 { 'status': 1000, data: 'xxx }
    # 其它 { 'status': 1001 }
    # 錯誤 { 'status': 1002 }
    @staticmethod
    def success(data):
        return {
            'status': 1000,
            'data': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 1002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 1001,
            'data': data
        }


class ArticleMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 2000,
            'data': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 2002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 2001,
            'data': data
        }


class CollectionMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 3000,
            'data': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 3002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 3001,
            'data': data
        }
