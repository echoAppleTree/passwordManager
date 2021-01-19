"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Authentification Functions for Password Manager
"""

import credential


def authentication(uname):
    """Verify if authorized user"""
    
    u1_username = credential.u1.name
    u1_secret_question = credential.u1.secret_question
    u1_secret_answer = credential.u1.secret_answer

    #authentification for David
    if u1_username == uname:
        answer = input("Secret Question: {} ".format(u1_secret_question))
        if answer == u1_secret_answer:
            return True
        else:
            False
    else:
        return False
