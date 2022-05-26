% include('header.tpl', title = "TODO app")
<h1>TODO app</h1>
<p><a href="/register">Acceso al formulario de registro</a></p>
<p><a href="/upload">subir archivo</a></p>
<p><b>Añadir una nueva tarea:</b></p>
<form action="/new" method="POST">
    <input type="text" size="70" maxlength="100" name="task">
    <input type="submit" name="save" value="Guardar">
</form>
<p><b>Las tareas actuales son las siguientes:</b></p>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Tarea</th>
        <th>Estado</th>
        <th colspan="3">Acciones</th>
    </tr>
    %for row in rows:
    <tr>
        <td>{{row[0]}}</td>
        %if row[2] == 0:
            <td class="finalizado">{{row[1]}}</td>
            <td>Cerrada</td>
        %else:
            <td>{{row[1]}}</td>
            <td>Abierta</td>
        %end
            
        <td>
            <form action="/edit/{{row[0]}}" method="GET">
                <input type="submit" name="save" value="Editar">
            </form>
        </td>
        <td>
            <form action="/delete/{{row[0]}}" method="GET">
                <input type="submit" name="delete" value="Borrar">
            </form>
        </td>
        <td>
            %if row[2] == 0:
                <form action="/open/{{row[0]}}" method="POST">
                    <input type="submit" name="open" value="Abrir">
                </form>
            %else:
                <form action="/close/{{row[0]}}" method="POST">
                    <input type="submit" name="close" value="Cerrar">
                </form>
            %end
        </td>
    </tr>
    %end
</table>
% include('footer.tpl')