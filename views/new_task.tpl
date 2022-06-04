% include('header.tpl', title = "Nueva tarea")

    <p>Añadir una nueva tarea a la lista:</p>
    <form action="/new" method="POST">
      <fieldset>
        <div>    
            {{ form.task.label }}:
            {{ form.task }}
            %if form.task.errors:
            <ul class="errors">
                %for error in form.task.errors:
                    <li>{{ error }}</li>
                %end
            </ul>
            %end
        </div>
        
    
        <div>
            {{ form.save }}
            
        </div>
        <div><a href="/" class="btn btn-secondary">Cancelar</a></div>
    </fieldset>
    </form>   

% include('footer.tpl')