from fpdf import FPDF

def pdfUsuario(nombre,correo,direccion,fecha,listaPedidos):
    pdf = FPDF(orientation= 'P', unit='mm', format='A4')

    pdf.add_page()

    pdf.set_font('Times')

    textoInicial = (
    f"Señor(a) administrador, bienvenido al reporte de PDF para usuarios\n"
    f"Nombre Usuario: {nombre}\n"
    f"Correo Usuario: {correo}\n"
    f"Direccion Usuario: {direccion}\n"
    f"Fecha y hora creacion Usuario: {fecha}"
    )

    pdf.multi_cell(w = 0, h = 10, txt = textoInicial, border = 0,
         align = 'L', fill = 0)
    
    # titulo
    pdf.cell(w = 0, h = 16, txt = 'Pedidos Realizados', border = 1, ln=1,
            align = 'C', fill = 0)

    # encabezado
    pdf.cell(w = 30, h = 13, txt = 'Origen', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 30, h = 13, txt = 'Destino', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 18, h = 13, txt = 'Paquetes', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 35, h = 13, txt = 'Fecha', border = 1,
            align = 'C', fill = 0)
    
    pdf.multi_cell(w = 0, h = 13, txt = 'Descripcion', border = 1,
            align = 'C', fill = 0)
    
    for pedido in listaPedidos:
        
        pdf.cell(w = 30, h = 11, txt = pedido.Origen, border = 1,
            align = 'C', fill = 0)

        pdf.cell(w = 30, h = 11, txt = pedido.Destino, border = 1,
                align = 'C', fill = 0)

        pdf.cell(w = 18, h = 11, txt = str(pedido.NumPaquetes), border = 1,
                align = 'C', fill = 0)

        pdf.cell(w = 35, h = 11, txt = str(pedido.FechaHoraSolicitud)[:10], border = 1,
                align = 'C', fill = 0)
        
        pdf.multi_cell(w = 0, h = 11, txt = pedido.Descripcion , border = 1,
                align = 'C', fill = 0)
    

    pdf.output('enviar/lastReport.pdf')


def pdfMensajero(nombre,correo,direccion,fecha,listaPedidos):
    pdf = FPDF(orientation= 'P', unit='mm', format='A4')

    pdf.add_page()

    pdf.set_font('Times')

    textoInicial = (
    f"Señor(a) administrador, bienvenido al reporte de PDF para mensajeros\n"
    f"Nombre Mensajero: {nombre}\n"
    f"Correo Mensajero: {correo}\n"
    f"Direccion Mensajero: {direccion}\n"
    f"Fecha y hora creacion Mensajero: {fecha}"
    )

    pdf.multi_cell(w = 0, h = 10, txt = textoInicial, border = 0,
         align = 'L', fill = 0)
    
    # titulo
    pdf.cell(w = 0, h = 16, txt = 'Pedidos Atendidos', border = 1, ln=1,
            align = 'C', fill = 0)

    # encabezado 
    pdf.cell(w = 30, h = 13, txt = 'Origen', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 30, h = 13, txt = 'Destino', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 20, h = 13, txt = 'Paquetes', border = 1,
            align = 'C', fill = 0)

    pdf.cell(w = 32, h = 13, txt = 'Transporte', border = 1,
            align = 'C', fill = 0)
    
    pdf.multi_cell(w = 0, h = 13, txt = 'Descripcion', border = 1,
            align = 'C', fill = 0)

    for pedido in listaPedidos:
        
        pdf.cell(w = 30, h = 11, txt = pedido.Origen, border = 1,
            align = 'C', fill = 0)

        pdf.cell(w = 30, h = 11, txt = pedido.Destino, border = 1,
                align = 'C', fill = 0)

        pdf.cell(w = 20, h = 11, txt = str(pedido.NumPaquetes), border = 1,
                align = 'C', fill = 0)

        pdf.cell(w = 32, h = 11, txt = pedido.TipoTransporte, border = 1,
                align = 'C', fill = 0)
        
        pdf.multi_cell(w = 0, h = 11, txt = pedido.Descripcion , border = 1,
                align = 'C', fill = 0)

    pdf.output('enviar/lastReport.pdf')
