import bardapi

token =  'ZQg_OUmxOnKyKP8-v8XNuaUm2r9v4ZPmUwIItY4Reto4LGl2IkrcTxSL9iaspMtnhHd6nw.'

def generate_letter(input_prompt):

    response = bardapi.Bard(token).get_answer(input_prompt)
    return(response['content'])

if __name__ == "__main__":
    input_prompt = "Hey write me simple qutoe about life"
    print(generate_letter(input_prompt))
