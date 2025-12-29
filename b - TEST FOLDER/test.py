<h1>HOLAAAA</h1>
<form action = {% url 'accounting:add_accounts' %} method = "POST">
    {% csrf_token %}
    <label for="my_test">That's my test</label>
    <input id="my_test" type="text" name="test_value">

</form>