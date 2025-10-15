<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';

const requests = ref([]);
const rooms = ref([])
const staff = ref([])
const statusOptions = ref([
	{ value: 'new', label: 'Новая' },
	{ value: 'in_progress', label: 'В процессе' },
	{ value: 'completed', label: 'Завершена' },
	{ value: 'cancelled', label: 'Отменена' }
]);

const requestToAdd = ref({
	date: '',
	description: '',
	status: 'new',
	room: null,
	staff: null
});
const requestToEdit = ref({
	date: '',
	description: '',
	status: null,
	room: null,
	staff: null
});
const stats = ref({});

const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);
const filters = ref({
	description: "",
	year: "",
	month: "",
	day: "",
	status: "",
	room: "",
	staff: "",
	user: ""
});

const filteredRequests = computed(() => {
	return requests.value.filter(item => {
		const matchesDescription = !filters.value.description || item.description.toLowerCase().includes(filters.value.description.toLowerCase());
		const matchesStatus = !filters.value.status || item.status === filters.value.status;
		const matchesRoom = !filters.value.room || item.room.id === filters.value.room;
		const matchesStaff = !filters.value.staff || item.staff.id === filters.value.staff;

		const itemDate = new Date(item.date);
		const matchesYear = !filters.value.year || itemDate.getFullYear() === parseInt(filters.value.year);
		const matchesMonth = !filters.value.month || itemDate.getMonth() + 1 === parseInt(filters.value.month);
		const matchesDay = !filters.value.day || itemDate.getDate() === parseInt(filters.value.day);

		const matchesUser = !filters.value.user || item.user === filters.value.user
		return matchesDescription && matchesStatus && matchesRoom && matchesStaff && matchesYear && matchesMonth && matchesDay && matchesUser;
	});
});

const getYears = () => {
	const years = new Set();
	requests.value.forEach(request => {
		const year = new Date(request.date).getFullYear();
		years.add(year);
	});
	return Array.from(years).sort();
};

const getMonths = () => {
	return [
		{ value: '1', label: 'Январь' },
		{ value: '2', label: 'Февраль' },
		{ value: '3', label: 'Март' },
		{ value: '4', label: 'Апрель' },
		{ value: '5', label: 'Май' },
		{ value: '6', label: 'Июнь' },
		{ value: '7', label: 'Июль' },
		{ value: '8', label: 'Август' },
		{ value: '9', label: 'Сентябрь' },
		{ value: '10', label: 'Октябрь' },
		{ value: '11', label: 'Ноябрь' },
		{ value: '12', label: 'Декабрь' },
	];
};

const getDays = () => {
	const days = new Set();
	requests.value.forEach(request => {
		const day = new Date(request.date).getDate();
		days.add(day);
	});
	return Array.from(days).sort();
};

async function fetchStats() {
	const r = await axios.get("/api/repairRequests/stats/");
	stats.value = r.data;
}
async function fetchRequests() {
	const r = await axios.get("/api/repairRequests/")
	requests.value = r.data
}

async function fetchRooms() {
	const r = await axios.get("/api/rooms/")
	rooms.value = r.data
}

async function fetchStaff() {
	const r = await axios.get("/api/staff/")
	staff.value = r.data
}

async function onRequestAdd() {
	await axios.post("/api/repairRequests/", {
		...requestToAdd.value
	});
	await fetchRequests();
}

async function onRequestRemoveClick(request) {
	await axios.delete(`/api/repairRequests/${request.id}/`);
	await fetchRequests();
}

async function onRequestEditClick(request) {
	requestToEdit.value = {
		id: request.id,
		date: request.date,
		description: request.description,
		status: request.status,
		room_id: request.room.id,
		staff_id: request.staff.id
	};
}

async function OnUpdateRequestClick() {
	await axios.put(`/api/repairRequests/${requestToEdit.value.id}/`, {
		...requestToEdit.value,
	});
	await fetchRequests();
}

onBeforeMount(async () => {
	await fetchRequests()
	await fetchRooms()
	await fetchStaff()
})
</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onRequestAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="requestToAdd.description" required>
						<label for="floatingInput">Описание проблемы</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<input type="date" class="form-control" v-model="requestToAdd.date" required>
						<label for="floatingInput">Дата</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.status" required>
							<option :value="option.value" v-for="option in statusOptions" :key="option.value">{{ option.label }}
							</option>
						</select>
						<label for="floatingInput">Статус заявки</label>
					</div>
				</div>
				<div class="col-1">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.room_id" required>
							<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
						</select>
						<label for="floatingInput">Комната</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.staff_id" required>
							<option :value="s.id" v-for="s in staff">{{ s.post }}({{ s.name }})</option>
						</select>
						<label for="floatingInput">Персонал</label>
					</div>
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
		<div class="mt-3">
			<h6 class="mb-1">Фильтры</h6>
			<div class="row pt-2 g-2 align-items-center">
				<div class="col d-flex gap-2">
					<input type="text" class="form-control" v-model="filters.description"
						placeholder="Фильтр по описанию проблемы" />
					<select class="form-select" v-model="filters.year">
						<option value="">Все года</option>
						<option v-for="year in getYears()" :key="year" :value="year">{{ year }}</option>
					</select>
					<select class="form-select" v-model="filters.month">
						<option value="">Все месяцы</option>
						<option v-for="month in getMonths()" :key="month.value" :value="month.value">{{ month.label }}</option>
					</select>
					<select class="form-select" v-model="filters.day">
						<option value="">Все дни</option>
						<option v-for="day in getDays()" :key="day" :value="day">{{ day }}</option>
					</select>
				</div>
			</div>
		</div>
		<div class="row pt-2 mb-2 g-2 align-items-center">
			<div class="col d-flex gap-2">
				<select class="form-select" v-model="filters.status">
					<option value="">Все статусы</option>
					<option v-for="option in statusOptions" :key="option.value" :value="option.value">{{ option.label }}
					</option>
				</select>
				<select class="form-select" v-model="filters.room">
					<option value="">Все комнаты</option>
					<option v-for="r in rooms" :key="r.id" :value="r.id">{{ r.number }}</option>
				</select>
				<select class="form-select" v-model="filters.staff">
					<option value="">Все сотрудники</option>
					<option v-for="s in staff" :key="s.id" :value="s.id">{{ s.post }} ({{ s.name }})</option>
				</select>
				<select class="form-select" v-model="filters.user" v-if="isSuperuser">
					<option value="">Все пользователи</option>
					<option :value="user.id" v-for="user in users" :key="user.id">{{ user.username }}</option>
				</select>
			</div>

		</div>
		<div class="row pt-2">
			<div class="col">
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
						data-bs-target="#statsModal">Статистика</button>
				</div>
			</div>
		</div>
	</div>

	<div>
		<div v-for="item in filteredRequests" class="request-item" :key="item.id">
			<div>{{ item.description }}</div>
			<div>{{ item.date }}</div>
			<div>{{ item.status_display }}</div>
			<div>{{ item.room.number }}</div>
			<div>{{ item.staff.post }} ({{ item.staff.name }})</div>
			<div>
				<button class="btn btn-success" @click="onRequestEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editRequestModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onRequestRemoveClick(item)">
					<i class="bi bi-trash"></i>
				</button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editRequestModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="requestToEdit.description" required>
								<label for="floatingInput">Описание проблемы</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col-4">
							<div class="form-floating">
								<input type="date" class="form-control" v-model="requestToEdit.date" required>
								<label for="floatingInput">Дата</label>
							</div>
						</div>
						<div class="col-4">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.status" required>
									<option :value="option.value" v-for="option in statusOptions" :key="option.value">{{ option.label }}
									</option>
								</select>
								<label for="floatingInput">Статус заявки</label>
							</div>
						</div>
						<div class="col-4">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.room_id" required>
									<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
								</select>
								<label for="floatingInput">Комната</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.staff_id" required>
									<option :value="s.id" v-for="s in staff">{{ s.post }}({{ s.name }})</option>
								</select>
								<label for="floatingInput">Персонал</label>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="OnUpdateRequestClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для статистики -->
	<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Статистика заявок</h5>
				</div>
				<div class="modal-body">
					<p>Количество заявок: {{ stats.count }}</p>
					<p>Максимальный ID заявки: {{ stats.max }}</p>
					<p>Минимальный ID заявки: {{ stats.min }}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
.request-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.7fr 0.3fr 0.3fr 0.3fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}
</style>