
class UserMessage(object):
    # 嚮應狀態碼規定
    # 嚮應給前端的，已1開頭，
    # 成功 { 'status': 1000, data: 'xxx }
    # 其它 { 'status': 1001 }
    # 錯誤 { 'status': 1002 }
    @staticmethod
    def success(data, action):
        return {
            'status': 1000,
            'data': data,
            'action': action
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

    # @staticmethod
    # def drafted_success(data, aid):
    #     return {
    #         'status': 2003,
    #         'data': data,
    #         'aid': aid
    #     }

    @staticmethod
    def saved_success(data, aid, data_list):
        return {
            'status': 2003,
            'data': data,
            'aid': aid,
            'list': data_list
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


class PraiseMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 4000,
            'praisedNum': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 4002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 4001,
            'data': data
        }


class ConcernMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 5000,
            'praisedNum': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 5002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 5001,
            'data': data
        }


class CommentMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 6000,
            'data': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 6002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 6001,
            'data': data
        }


class PersonalMessage(object):
    @staticmethod
    def success(data):
        return {
            'status': 7000,
            'data': data
        }

    @staticmethod
    def fail(data):
        return {
            'status': 7002,
            'data': data
        }

    @staticmethod
    def other(data):
        return {
            'status': 7001,
            'data': data
        }
