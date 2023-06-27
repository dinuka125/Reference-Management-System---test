import bardapi

token =  'YAg_OQmFUn--EklOAmddtngCgUQGmo3Y69JaoeYMOyGqb0wJlynTyvj1jFZM2l4fpb7eDw.'

def generate_letter(input_prompt):

    response = bardapi.Bard(token).get_answer(input_prompt)
    return(response['content'])

if __name__ == "__main__":
    input_prompt = "Hey write me simple qutoe about life"
    print(generate_letter(input_prompt))
