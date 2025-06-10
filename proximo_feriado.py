import requests
from datetime import date

def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"

months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']

def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]

class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays, type=None):
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        
        if type is None:
            holiday = next(
                (h for h in holidays if h['mes'] == today['month'] and h['dia'] > today['day'] 
                or h['mes'] > today['month']), holidays[0])
            self.loading = False
        else:
            holiday = next(
                (h for h in holidays if (h['mes'] == today['month'] and h['dia'] > today['day'] or 
                h['mes'] > today['month']) and h['tipo'].lower() == type.lower()), None)

            if holiday is not None:
                self.loading = False
            else:
                holiday = f"No hay feriados para el año {self.year} de tipo {type}"
        
        self.holiday = holiday


        # NOTE - type determina el tipo de feriado que buscamos
    def fetch_holidays(self, type=None):
        response = requests.get(get_url(self.year))
        data = response.json()

        # NOTE - if type != inamovible | trasladable | nolaborable | puente
        # then type = None 
        parametter = type if type else None 
        self.set_next(data,parametter)

    
    def render(self):
        if self.loading:
            print("Buscando...")
            print(self.holiday) 
        
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'], self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])

def main():
    # SECTION - main call 
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    next_holiday.render()

if __name__ == "__main__":
    main()
