class PlanificadorFuerzaLaboral:
    def __init__(self, requerimientos, c_mantener, c_fijo, c_var):
        self.reqs = requerimientos
        self.n = len(requerimientos)
        self.c_m = c_mantener
        self.c_f = c_fijo
        self.c_v = c_var
        self.max_req = max(requerimientos)
        self.memoria = {}
        self.bitacora = []

    def _calc_contratacion(self, anterior, actual):
        if actual > anterior:
            return self.c_f + self.c_v * (actual - anterior)
        return 0

    def _calc_exceso(self, actual, requerido):
        return self.c_m * (actual - requerido)

    def _registrar(self, mensaje):
        self.bitacora.append(mensaje)
        print(mensaje)

    def optimizar(self):
        self._registrar("=== OPTIMIZACIÓN DE FUERZA LABORAL ===")
        self.memoria[self.n + 1] = {x: (0, 0) for x in range(self.max_req + 1)}

        for i in range(self.n, 0, -1):
            req_actual = self.reqs[i-1]
            self._registrar(f"\n--- Semana {i} | Requerimiento: {req_actual} ---")
            self.memoria[i] = {}

            estados = [0] if i == 1 else range(self.reqs[i-2], self.max_req + 1)
            
            self._registrar(f"{'Previo':<7}| {'Actual':<7}| {'C.Contrato':<11}| {'C.Exceso':<10}| {'Futuro':<8}| {'C.Total':<8}| {'Opt'}")
            
            for previo in estados:
                mejor_c = float('inf')
                mejor_d = -1
                resultados = []

                decisiones = [req_actual] if i == self.n else range(req_actual, self.max_req + 1)

                for actual in decisiones:
                    c_cont = self._calc_contratacion(previo, actual)
                    c_exc = self._calc_exceso(actual, req_actual)
                    c_fut = self.memoria[i+1][actual][0]
                    c_tot = c_cont + c_exc + c_fut

                    resultados.append((actual, c_cont, c_exc, c_fut, c_tot))

                    if c_tot < mejor_c:
                        mejor_c = c_tot
                        mejor_d = actual

                self.memoria[i][previo] = (mejor_c, mejor_d)

                for r in resultados:
                    act, cc, ce, cf, ct = r
                    marca = "<--" if act == mejor_d and ct == mejor_c else ""
                    self._registrar(f"{previo:<7}| {act:<7}| {cc:<11}| {ce:<10}| {cf:<8}| {ct:<8}| {marca}")

        self.imprimir_ruta()

    def imprimir_ruta(self):
        self._registrar("\n--- POLÍTICA ÓPTIMA ---")
        estado = 0
        self._registrar(f"Costo Total: ${self.memoria[1][0][0]}\n")
        
        for i in range(1, self.n + 1):
            decision = self.memoria[i][estado][1]
            accion = "Contrata" if decision > estado else "Mantiene/Reduce"
            self._registrar(f"Semana {i}: Tenía {estado} -> {accion} a {decision} (Req: {self.reqs[i-1]})")
            estado = decision

    def guardar_txt(self, archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.bitacora))
        print(f"\n[OK] Resultados guardados en '{archivo}' para subir a Acrópolis.")


if __name__ == "__main__":
    reqs_semanales = [5, 7, 8, 4, 6] 
    mantener = 300 
    fijo_contratar = 400 
    var_contratar = 200 
    
    sistema = PlanificadorFuerzaLaboral(reqs_semanales, mantener, fijo_contratar, var_contratar)
    sistema.optimizar()
    sistema.guardar_txt("Salida_FuerzaLaboral.txt")