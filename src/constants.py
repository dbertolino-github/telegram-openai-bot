#: It contains the initial prompt to set up a conversation with ChatGPT
INIT_CHATBOT_PROMPT = """
    [PROMPT PER INIZIALIZZARE IL COMPORTAMENTO DEL BOT, e.g. Stai impersonando un giornalista che chiede informazioni riguardo un avvenimento... Io sono una persona di nome {}]
    """ 

#: It contains the summary prompt for ChatGPT, in other words the rules that ChatGPT must follow while gnerating a report
SUMMARY_PROMPT = """
    Data la seguente conversazione: {} 
    Genera un riassunto di massimo 300 caratteri con i principali punti affrontati sui principali argomenti discussi.
    Date le informazioni contenute nella conversazione, concludi il riassunto con il grado di pericolosità della conversazione.
    Il grado di pericolosità deve essere indicato solo come 'Alto', 'Medio' o 'Basso' nel seguente formato: _SEVERITY_: <grado_severity>
    """

