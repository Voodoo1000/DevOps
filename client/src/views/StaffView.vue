<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';

const staff = ref([]);
const staffToAdd = ref({
	name: '',
	post: ''
});
const staffToEdit = ref({
	name: '',
	post: ''
});
const staffPictureRef = ref();
const staffPictureRefEdit = ref();
const staffAddImageUrl = ref();
const staffEditImageUrl = ref();
const selectedImageUrl = ref();
const stats = ref({});

const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);
const filters = ref({
	name: "",
	post: "",
	user: ""
});

const filteredStaff = computed(() => {
	return staff.value.filter((member) => {
		return (
			(!filters.value.name || member.name.toLowerCase().includes(filters.value.name.toLowerCase())) &&
			(!filters.value.post || member.post.toLowerCase().includes(filters.value.post.toLowerCase())) &&
			(!filters.value.user || member.user === filters.value.user)
		);
	});
});

function openImageModal(imageUrl) {
	selectedImageUrl.value = imageUrl;
	const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
	imageModal.show();
}

async function fetchStaff() {
	const r = await axios.get("/api/staff/")
	staff.value = r.data
}
async function fetchStats() {
	const r = await axios.get("/api/staff/stats/");
	stats.value = r.data;
}
async function onStaffAdd() {
	const formData = new FormData();

	formData.append('picture', staffPictureRef.value.files[0]);

	formData.set('name', staffToAdd.value.name)
	formData.set('post', staffToAdd.value.post)

	await axios.post("/api/staff/", formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStaff();
}

async function staffAddPictureChange() {
	staffAddImageUrl.value = URL.createObjectURL(staffPictureRef.value.files[0])
}
async function staffEditPictureChange() {
	staffEditImageUrl.value = URL.createObjectURL(staffPictureRefEdit.value.files[0])
}

async function onStaffRemoveClick(staff) {
	await axios.delete(`/api/staff/${staff.id}/`);
	await fetchStaff();
}

async function onStaffEditClick(staff) {
	staffToEdit.value = {
		id: staff.id,
		name: staff.name,
		post: staff.post,
		picture: staff.picture
	};
	staffEditImageUrl.value = staff.picture;
}

async function OnUpdateStaffClick() {
	const formData = new FormData();

	formData.append('picture', staffPictureRefEdit.value.files[0]);

	formData.set('name', staffToAdd.value.name)
	formData.set('post', staffToAdd.value.post)

	await axios.put(`/api/staff/${staffToEdit.value.id}/`, formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStaff();
}

onBeforeMount(async () => {
	await fetchStaff()
})

</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onStaffAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="staffToAdd.name" required>
						<label for="floatingInput">ФИО</label>
					</div>
				</div>
				<div class="col-3">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="staffToAdd.post" required>
						<label for="floatingInput">Должность</label>
					</div>
				</div>
				<div class="col-3">
					<input class="form-control" type="file" ref="staffPictureRef" @change="staffAddPictureChange()" required>
				</div>
				<div class="col-auto">
					<img :src="staffAddImageUrl" style="max-height: 60px;" alt="">
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
		<div class="mt-3">
			<h6 class="mb-1">Фильтры</h6>
			<div class="row pt-2 mb-2 g-2 align-items-center">
				<div class="col d-flex gap-2">
					<input type="text" class="form-control" v-model="filters.name" placeholder="Фильтр по имени" />
					<input type="text" class="form-control" v-model="filters.post" placeholder="Фильтр по должности" />
					<select class="form-select" v-model="filters.user" v-if="isSuperuser">
						<option value="">Все пользователи</option>
						<option :value="user.id" v-for="user in users" :key="user.id">{{ user.username }}</option>
					</select>
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
						data-bs-target="#statsModal">Статистика</button>
				</div>
			</div>
		</div>
	</div>

	<div>
		<div v-for="item in filteredStaff" :key="item.id" class="staff-item">
			<div>
				{{ item.name }}
			</div>
			<div>
				{{ item.post }}
			</div>
			<div v-show="item.picture">
				<img :src="item.picture" style="max-height: 60px;" @click="openImageModal(item.picture)"
					alt="Картинка персонала" data-bs-toggle="modal" data-bs-target="#imageModal">
			</div>
			<div class="d-flex justify-content-end">
				<button class="btn btn-success me-1" @click="onStaffEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editStaffModal">
					<i class="bi bi-pen"></i>
				</button>
				<button class="btn btn-danger" @click="onStaffRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editStaffModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="staffToEdit.name">
								<label for="floatingInput">ФИО</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="staffToEdit.post">
								<label for="floatingInput">Должность</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col-6">
							<input class="form-control" type="file" ref="staffPictureRefEdit" @change="staffEditPictureChange()"
								required>
						</div>
						<div class="col-auto">
							<img :src="staffEditImageUrl" style="max-height: 60px;" alt="">
						</div>
					</div>
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
					@click="OnUpdateStaffClick()">Сохранить</button>
			</div>
		</div>
	</div>
	<!-- Модальное окно для просмотра картинки -->
	<div class="modal fade" id="imageModal" tabindex="-1" role="dialog">
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-body text-center">
					<img :src="selectedImageUrl" alt="Просмотр изображения" class="img-fluid">
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для статистики -->
	<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Статистика персонала</h5>
				</div>
				<div class="modal-body">
					<p>Количество комнат: {{ stats.count }}</p>
					<p>Максимальный ID персонала: {{ stats.max }}</p>
					<p>Минимальный ID персонала: {{ stats.min }}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
.staff-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.5fr 0.25fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}

.staff-item img {
	cursor: pointer;
}
</style>