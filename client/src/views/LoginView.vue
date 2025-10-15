<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';
import Cookies from 'js-cookie'; 

const user = ref("");
const password = ref("");
const userStore = useUserStore();
const { isAuthenticated, username, userId } = storeToRefs(userStore);
const router = useRouter();

import { useToast } from 'vue-toastification';

const toast = useToast();

async function login() {
    const csrfToken = Cookies.get('csrftoken'); 

    try {
        const response = await axios.post("/api/user/login/", {
            user: user.value,
            password: password.value
        }, {
            headers: {
                'X-CSRFToken': csrfToken 
            }
        });

        if (response.status === 200) {
            await userStore.fetchUser();
            toast.success("Успешный вход!");
            router.push("/");
        } else {
            toast.error("Ошибка входа: " + response.data);
        }
    } catch (error) {
        console.error("Ошибка входа:", error);
        toast.error("Ошибка входа, попробуйте еще раз.");
    }
}
</script>


<template>
	<div class="container-fluid">
		<div class="col-md-4 offset-md-4">
			<div class="form-container">
				<div class="form-icon"><i class="fa fa-user"></i></div>
				<h3 class="title">Вход</h3>
				<form class="form-horizontal" @submit.prevent="login">
					<div class="form-group">
						<label>Логин</label>
						<input class="form-control" type="login" placeholder="Введите логин" v-model="user" required>
					</div>
					<div class="form-group">
						<label>Пароль</label>
						<input class="form-control" type="password" placeholder="Введите пароль" v-model="password" required>
					</div>
					<button type="submit" class="btn btn-default">Вход</button>
				</form>
			</div>
		</div>
	</div>
</template>

<style>
.form-container {
	background: #ecf0f3;
	font-family: 'Nunito', sans-serif;
	padding: 40px;
	border-radius: 20px;
	box-shadow: 14px 14px 20px #cbced1, -14px -14px 20px white;
}

.form-container .form-icon {
	color: #ac40ab;
	font-size: 55px;
	text-align: center;
	line-height: 100px;
	width: 100px;
	height: 100px;
	margin: 0 auto 15px;
	border-radius: 50px;
	box-shadow: 7px 7px 10px #cbced1, -7px -7px 10px #fff;
}

.form-container .title {
	color: #ac40ab;
	font-size: 25px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 1px;
	text-align: center;
	margin: 0 0 20px;
}

.form-container .form-horizontal .form-group {
	margin: 0 0 25px 0;
}

.form-container .form-horizontal .form-group label {
	font-size: 15px;
	font-weight: 600;
	text-transform: uppercase;
}

.form-container .form-horizontal .form-control {
	color: #333;
	background: #ecf0f3;
	font-size: 15px;
	height: 50px;
	padding: 20px;
	letter-spacing: 1px;
	border: none;
	border-radius: 50px;
	box-shadow: inset 6px 6px 6px #cbced1, inset -6px -6px 6px #fff;
	display: inline-block;
	transition: all 0.3s ease 0s;
}

.form-container .form-horizontal .form-control:focus {
	box-shadow: inset 6px 6px 6px #cbced1, inset -6px -6px 6px #fff;
	outline: none;
}

.form-container .form-horizontal .form-control::placeholder {
	color: #808080;
	font-size: 14px;
}

.form-container .form-horizontal .btn {
	color: #000;
	background-color: #ac40ab;
	font-size: 15px;
	font-weight: bold;
	text-transform: uppercase;
	width: 100%;
	padding: 12px 15px 11px;
	border-radius: 20px;
	box-shadow: 6px 6px 6px #cbced1, -6px -6px 6px #fff;
	border: none;
	transition: all 0.5s ease 0s;
}

.form-container .form-horizontal .btn:hover,
.form-container .form-horizontal .btn:focus {
	color: #fff;
	letter-spacing: 3px;
	box-shadow: none;
	outline: none;
}
</style>
