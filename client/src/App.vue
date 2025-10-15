<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from './stores/userStore';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import Cookies from 'js-cookie'; 
import { ref } from 'vue';

const userStore = useUserStore();
const { isAuthenticated,	username,	userId } = storeToRefs(userStore);
const toast = useToast();

async function logout() {
    const csrfToken = Cookies.get('csrftoken');
    try {
        const response = await axios.post('/api/user/logout/', {}, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        if (response.data.success) {
            userStore.resetUser();
            window.location.reload();
        } else {
            toast.error('Ошибка выхода, попробуйте еще раз.');
        }
    } catch (error) {
        console.error('Ошибка выхода:', error);
        toast.error('Ошибка выхода, попробуйте еще раз.');
    }

		
}
const showCatModal = ref(false);
const catImageUrl = ref('');

async function fetchRandomCat() {
    try {
        const response = await axios.get('https://api.thecatapi.com/v1/images/search');
        catImageUrl.value = response.data[0].url;
        showCatModal.value = true;
    } catch (error) {
        console.error('Ошибка загрузки котика:', error);
        toast.error('Не удалось загрузить котика :(');
    }
}

function closeCatModal() {
    showCatModal.value = false;
}
</script>
<template>
	<div class="container">
		<nav class="navbar navbar-expand-lg bg-body-tertiary">
			<div class="container-fluid">
				<a class="navbar-brand">Общежитие</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
					aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse justify-content-between" id="navbarNav">
					<ul class="navbar-nav">
						<li class="nav-item">
							<router-link class="nav-link" to="/">Студенты</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/rooms">Комнаты</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/dutySchedule">График дежурств</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/staff">Персонал общежития </router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/repairRequests">Заявки на ремонт</router-link>
						</li>
					</ul>
					<ul class="navbar-nav">
						<li class="nav-item dropdown">
							<a class="nav-item dropdown-toggle link" href="#" role="button" data-bs-toggle="dropdown"	aria-expanded="false">
								{{ username }}
							</a>
							<ul class="dropdown-menu">
								<li class="nav-item"><router-link class="dropdown-item" to="/login">Войти</router-link></li>
								<li class="nav-item"><a class="dropdown-item" @click.prevent="logout()">Выход</a></li>
								<li><a class="dropdown-item" href="/admin">Админка</a></li>
							</ul>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	</div>
	<div class="container">
		<router-view />
	</div>

	<div class="cat-button" @click="fetchRandomCat">
		🐾
	</div>

	<div v-if="showCatModal" class="cat-modal">
	<div class="cat-modal-content">
		<img :src="catImageUrl" alt="Random Cat" />
		<div class="button-container">
			<button @click="closeCatModal">Закрыть</button>
		</div>
	</div>
</div>
</template>

<style lang="scss" scoped>
.link {
	text-decoration: none;
	color: #666;
}
.cat-button {
	position: fixed;
	bottom: 20px;
	right: 20px;
	background-color: #f0f0f0;
	border: 2px solid #ddd;
	border-radius: 50%;
	width: 60px;
	height: 60px;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
	font-size: 24px;
}

.cat-modal-content .button-container {
	width: 100%;
	margin-top: 10px;
	display: flex;
	justify-content: center;
}

.cat-button:hover {
	background-color: #e0e0e0;
}

.cat-modal {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.7);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.cat-modal-content {
	background: white;
	padding: 20px;
	border-radius: 10px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	text-align: center;
	display: flex;
	flex-direction: column;
	align-items: center;
	position: relative;
	z-index: 1001;
}

.cat-modal-content img {
	max-width: 300px;
	border-radius: 10px;
	margin-bottom: 15px;
}

.cat-modal-content button {
	padding: 10px 20px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.cat-modal-content button:hover {
	background-color: #0056b3;
}

body.modal-open {
	overflow: hidden;
}
</style>
