export const required = {
    required: {
        value: true,
        message: "Обязательное поле"
    }
}
export const email = {
    pattern: {
        value: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
        message: "Не верный email"
    }
}

export const date = {
    pattern: {
        value: /\d{4}-\d{2}-\d{2}$/,
        message: "Не верный email"
    }
}