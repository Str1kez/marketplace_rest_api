from starlette import status

VALIDATION_ERROR_RESPONSE = {400: {'description': "Validation Error",
                                   "content": {'application/json':
                                                   {"example":
                                                        {'code': status.HTTP_400_BAD_REQUEST,
                                                         'message': 'Validation Error'}
                                                    }
                                               }
                                   }}

NOT_FOUND_RESPONSE = {404: {'description': "Not Found",
                            "content": {'application/json':
                                            {"example":
                                                 {'code': status.HTTP_404_NOT_FOUND,
                                                  'message': 'Not Found'}
                                             }
                                        }
                            }
                      }
