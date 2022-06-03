% include('header.tpl', title = "registrarse")
<h1>Formulario de registro</h1>
% if form.errors:
<blockquote>
    <p>Hay errores en el formulario:</p>
    <ul>
    % for field, errors in form.errors.items():
        % for error in errors:
        <li>{{field}}: {{error}}</li>
        % end
    % end
    </ul>
</blockquote>

% end
<form method="POST" action="/register">
    <fieldset>
    

    <div>    
        {{ form.id.label }}:
        {{ form.id }}
        %if form.id.errors:
        <ul class="errors">
            %for error in form.id.errors:
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