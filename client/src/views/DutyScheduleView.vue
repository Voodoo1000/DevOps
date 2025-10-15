<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';

const students = ref([]);
const duty = ref([])
const dutyToAdd = ref({
	date: '',
	student: null
});
const dutyToEdit = ref({
	date: '',
	student: null
});
const stats = ref({});

const userStore = useUserStore();
const { isSuperuser, users } = storeToRefs(userStore);
const filters = ref({
	year: "",
	month: "",
	day: "",
	studentName: "",
	user: ""
});

const filteredDuty = computed(() => {
	return duty.value.filter(item => {
		const itemDate = new Date(item.date);
		const matchesYear = !filters.value.year || itemDate.getFullYear() === parseInt(filters.value.year);
		const matchesMonth = !filters.value.month || itemDate.getMonth() + 1 === parseInt(filters.value.month); 
		const matchesDay = !filters.value.day || itemDate.getDate() === parseInt(filters.value.day);

		const matchesStudent = !filters.value.studentName || item.student.name.toLowerCase().includes(filters.value.studentName.toLowerCase());

		const matchesUser = !filters.value.user || item.user === filters.value.user
		return matchesYear && matchesMonth && matchesDay && matchesStudent && matchesUser;
	});
});

const getYears = () => {
  const years = new Set();
  duty.value.forEach(item => {
    const year = new Date(item.date).getFullYear();
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
  duty.value.forEach(item => {
    const day = new Date(item.date).getDate();
    days.add(day);
  });
  return Array.from(days).sort();
};

async function fetchStats() {
	const r = await axios.get("/api/dutySchedule/stats/");
	stats.value = r.data;
}

async function fetchStudents() {
	const r = await axios.get("/api/students/")
	students.value = r.data
}

async function fetchDuty() {
	const r = await axios.get("/api/dutySchedule/")
	duty.value = r.data
}

async function onDutyAdd() {
	await axios.post("/api/dutySchedule/", {
		...dutyToAdd.value
	});
	await fetchDuty();
}

async function onDutyRemoveClick(duty) {
	await axios.delete(`/api/dutySchedule/${duty.id}/`);
	await fetchDuty();
}

async function onDutyEditClick(duty) {
	dutyToEdit.value = {
		id: duty.id,
		date: duty.date,
		student_id: duty.student.id,
	};
}

async function onUpdateDutyClick() {
	await axios.put(`/api/dutySchedule/${dutyToEdit.value.id}/`, {
		...dutyToEdit.value,
	});
	await fetchDuty();
}

onBeforeMount(async () => {
	await fetchStudents()
	await fetchDuty()
})
</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onDutyAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="date" class="form-control" v-model="dutyToAdd.date" required>
						<label for="floatingInput">Дата</label>
					</div>
				</div>
				<div class="col-5">
					<div class="form-floating">
						<select class="form-select" v-model="dutyToAdd.student_id" required>
							<option :value="s.id" v-for="s in students">{{ s.name }}</option>
						</select>
						<label for="floatingInput">Студент</label>
					</div>
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
				<input type="text" class="form-control" v-model="filters.studentName" placeholder="Фильтр по имени студента" />
				<select class="form-select" v-model="filters.user" v-if="isSuperuser">
          <option value="">Все пользователи</option>
          <option :value="user.id" v-for="user in users" :key="user.id">{{ user.username }}</option>
        </select>
			</div>
		</div>
	</div>
		<div class="row pt-2">
			<div class="col-auto d-flex align-self-center">
				<button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
					data-bs-target="#statsModal">Статистика</button>
			</div>
		</div>
	</div>

	<div>
		<div v-for="item in filteredDuty" :key="item.id" class="duty-item">
			<div>
				{{ item.date }}
			</div>
			<div>
				{{ item.student.name }}
			</div>
			<div>
				<button class="btn btn-success" @click="onDutyEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editDutyModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onDutyRemoveClick(item)">
					<i class="bi bi-trash"></i>
				</button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editDutyModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="date" class="form-control" v-model="dutyToEdit.date">
								<label for="floatingInput">Дата</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<select class="form-select" v-model="dutyToEdit.student_id" required>
									<option :value="r.id" v-for="r in students">{{ r.name }}</option>
								</select>
								<label for="floatingInput">Студент</label>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="onUpdateDutyClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для статистики -->
	<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Статистика графиков</h5>
				</div>
				<div class="modal-body">
					<p>Количество комнат: {{ stats.count }}</p>
					<p>Максимальный ID графиков: {{ stats.max }}</p>
					<p>Минимальный ID графиков: {{ stats.min }}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
.duty-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.5fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}
</style>