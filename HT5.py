import simpy
import random

Semilla = 0
Ram_Inicial = 100
Intervalo = 10
Velocidad = 3
Tiempos = []

random.seed(Semilla)

# entorno de simulación
env = simpy.Environment()

# simular la memoria RAM
RAM = simpy.Container(env, init=Ram_Inicial, capacity=Ram_Inicial)

# Simular el CPU/ procesador
CPU = simpy.Resource(env, capacity=1)

def Proceso(env, nombre, RAM, CPU):
    print(f"{nombre} llega al sistema en t = {env.now}")
    
    # Solicitar memoria RAM
    memoria_requerida = random.randint(1, 10)
    yield RAM.get(memoria_requerida)
    print(f"{nombre} obtiene {memoria_requerida} de memoria RAM en t = {env.now}")
    
    # Pasar a estado "Listo (ready)"
    with CPU.request() as req:
        yield req  # Esperar a que el CPU esté disponible
        print(f"{nombre} comienza a ejecutarse en el CPU en t = {env.now}")
        
        # Ejecutar instrucciones en el CPU
        instrucciones_restantes = random.randint(1, 10)
        while instrucciones_restantes > 0:  
            yield env.timeout(Velocidad)
            print(f"{nombre} ha ejecutado 3 instrucciones en t = {env.now}")
            
            # Actualizar el contador de instrucciones
            instrucciones_restantes -= 3
            if instrucciones_restantes <= 0:
                # El proceso ha terminado
                print(f"{nombre} ha terminado todas las instrucciones en t = {env.now}")

                # Lógica para determinar si Waiting, Ready o Terminated
                probabilidad_waiting = random.uniform(0, 1)
                if probabilidad_waiting <= 0.5:
                    # 50% de probabilidad de ir a Waiting
                    print(f"{nombre} va a la cola de Waiting")
                    yield env.timeout(1)  # Simula operaciones de I/O
                    print(f"{nombre} regresa a la cola de Ready desde Waiting")
                else:
                    # 50% de probabilidad de ir a Ready
                    print(f"{nombre} va a la cola de Ready")

                # Devolver la memoria RAM al finalizar
                yield RAM.put(memoria_requerida)
                print(f"{nombre} devuelve {memoria_requerida} de memoria RAM en t = {env.now}")
                print("\n")
                return

# Generador procesos
def llegada(env, RAM, CPU):
    # Ciclo infinito para simular llegada continua de procesos
    while True:
        proceso = env.process(Proceso(env, f"Proceso-{env.now}", RAM, CPU))
        Tiempo_llegada = env.now
        yield proceso
        Tiempos.append(env.now - Tiempo_llegada)

# Iniciar la simulación
env.process(llegada(env, RAM, CPU))
env.run(until=50)

# Calcular promedio y desviación estándar de tiempos de ejecución
promedio = sum(Tiempos) / len(Tiempos)
desviacion = (sum((t - promedio) ** 2 for t in Tiempos) / len(Tiempos)) ** 0.5

# Imprimir resultados
print("\n")
print(f"DATOS ESTADÍSTICOS DEL PROCESO:")
print(f"Promedio de tiempo de ejecución: {promedio}")
print(f"Desviación estándar: {desviacion}")