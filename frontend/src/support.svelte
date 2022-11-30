<script lang="ts">
  let errors: { [inputName: string]: any } = {};

  function isFormValid(data: { [inputName: string]: any }): boolean {
    return !Object.keys(errors).some((inputName) =>
      Object.keys(errors[inputName]).some(
        (errorName) => errors[inputName][errorName],
      ),
    );
  }

  function validateForm(data: { [inputName: string]: any }):void {
    if (!isRequiredFieldValid(data.name)) {
      errors['name'] = { ...errors['name'], required: true };
    } else {
      errors['name'] = { ...errors['name'], required: false };
    }

    if (!isRequiredFieldValid(data.surname)) {
      errors['surname'] = { ...errors['surname'], required: true };
    } else {
      errors['surname'] = { ...errors['surname'], required: false };
    }

    if (!isRequiredFieldValid(data.patronymic)) {
      errors['patronymic'] = { ...errors['patronymic'], required: true };
    } else {
      errors['patronymic'] = { ...errors['patronymic'], required: false };
    }

    if (!isRequiredFieldValid(data.phone_number)) {
      errors['phone_number'] = { ...errors['phone_number'], required: true };
    } else {
      errors['phone_number'] = { ...errors['phone_number'], required: false };
    }

    if (!isRequiredFieldValid(data.description)) {
      errors['description'] = { ...errors['description'], required: true };
    } else {
      errors['description'] = { ...errors['description'], required: false };
    }
  }

  function isRequiredFieldValid(value) {
    return value != null && value !== '';
  }

  async function onSubmit(e) {
    const formData = new FormData(e.target);

    const data: any = {};
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }

    validateForm(data);

    if (isFormValid(data)) {
      this.reset();
      const response = await fetch(this.action, {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData)),
      });
    } else {
      console.log('Invalid Form');
    }

  }
</script>


<form class="container" on:submit|preventDefault={onSubmit} action="http://127.0.0.1:8888/appeal">
  <div class="my-2 my-lg-0 bg-white shadow-soft border rounded border-gray-200 p-2 p-lg-3">
    <div class="text-center text-md-center mb-4 mt-md-0">
      <h1>Форма обращения</h1>
    </div>
    <div class="row">
      <div class="col-md-6">
        <label class="form-label mt-3">Имя</label>
        <input type="text" class="form-control" id="name" name="name">
        {#if errors.name && errors.name.required}
          <p class="error-message">Поле «Имя» является обязательным.</p>
        {/if}
      </div>
      <div class="col-md-6">
        <label class="form-label mt-3">Фамилия</label>
        <input type="text" class="form-control" id="surname" name="surname">
        {#if errors.surname && errors.surname.required}
          <p class="error-message">Поле «Фамилия» является обязательным.</p>
        {/if}
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <label class="form-label mt-3">Отчество</label>
        <input type="text" class="form-control" id="patronymic" name="patronymic">
        {#if errors.patronymic && errors.patronymic.required}
          <p class="error-message">Поле «Отчество» является обязательным.</p>
        {/if}
      </div>
      <div class="col-md-6">
        <label for="phone_number" class="form-label mt-3">Телефон</label>
        <input type="tel" class="form-control" id="phone_number" name="phone_number"
               minlength="10" maxlength="15" pattern="[0-9]+">
        {#if errors.phone_number && errors.phone_number.required}
          <p class="error-message">Поле «Телефон» является обязательным.</p>
        {/if}
      </div>
    </div>
    <div class="col-12">
      <label class="form-label mt-3">Обращение</label>
      <textarea class="form-control" id="description" name="description"></textarea>
      {#if errors.description && errors.description.required}
        <p class="error-message">Поле «Обращение» является обязательным.</p>
      {/if}
    </div>
    <div class="text-center">
      <input class="btn btn-primary mt-2" type="submit">
    </div>
  </div>
</form>


<style>

  .container {
      display: grid;
      grid-auto-flow: row;
      grid-gap: 0.5rem;
      grid-auto-rows: minmax(2rem, min-content);
  }

  .error-message {
    color: tomato;
    flex: 0 0 100%;
    margin: 0 2px;
    font-size: 0.8em;
  }
</style>