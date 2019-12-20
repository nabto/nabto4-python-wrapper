%module nabto_api
%{
    #include "../extension/inc/wrapper.h"
%}

%include <std_string.i>
%include "../extension/inc/wrapper.h"

%inline %{
struct Status {
    enum {
        NABTO_OK = 0,
        NABTO_NO_PROFILE = 1,
        NABTO_ERROR_READING_CONFIG = 2,
        NABTO_API_NOT_INITIALIZED = 3,
        NABTO_INVALID_SESSION = 4,
        NABTO_OPEN_CERT_OR_PK_FAILED = 5,
        NABTO_UNLOCK_PK_FAILED = 6,
        NABTO_PORTAL_LOGIN_FAILURE = 7,
        NABTO_CERT_SIGNING_ERROR = 8,
        NABTO_CERT_SAVING_FAILURE = 9,
        NABTO_ADDRESS_IN_USE = 10,
        NABTO_INVALID_ADDRESS = 11,
        NABTO_NO_NETWORK = 12,
        NABTO_CONNECT_TO_HOST_FAILED = 13,
        NABTO_STREAMING_UNSUPPORTED = 14,
        NABTO_INVALID_STREAM = 15,
        NABTO_DATA_PENDING = 16,
        NABTO_BUFFER_FULL = 17,
        NABTO_FAILED = 18,
        NABTO_INVALID_TUNNEL = 19,
        NABTO_ILLEGAL_PARAMETER = 20,
        NABTO_INVALID_RESOURCE = 21,
        NABTO_INVALID_STREAM_OPTION = 22,
        NABTO_INVALID_STREAM_OPTION_ARGUMENT = 23,
        NABTO_ABORTED = 24,
        NABTO_STREAM_CLOSED = 25,
        NABTO_FAILED_WITH_JSON_MESSAGE = 26,
        NABTO_ERROR_CODE_COUNT
    };
};
%}