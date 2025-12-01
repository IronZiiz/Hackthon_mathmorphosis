import json

class DataLogger:
    def __init__(self, feedback_value=None):
        self.feedback_value = feedback_value

    def save_feedback_to_json(self):
        filename = "feedback_log.json"

        if self.feedback_value == 1:
            _data = {"feedback": "Ótimo"}
        elif self.feedback_value == 0:
            _data = {"feedback": "Ruim"}
        else:
            return "Valor de feedback inválido."

        try:
            with open(filename, 'a+', encoding='utf-8') as f:
                json_record = json.dumps(_data, ensure_ascii=False)
                f.write(json_record + '\n')

            return f"Feedback salvo em {filename}"

        except Exception as e:
            return f"Erro ao salvar feedback: {str(e)}"
