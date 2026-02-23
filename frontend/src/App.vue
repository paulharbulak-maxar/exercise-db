<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { api } from "./api";

const loading = ref(false);
const saving = ref(false);
const error = ref("");

const programs = ref([]);
const exercises = ref([]);

const selectedProgramId = ref(null);
const templates = ref([]);
const selectedTemplateId = ref(null);
const templateExercises = ref([]);

const workouts = ref([]);
const selectedWorkoutId = ref(null);
const selectedWorkout = ref(null);
const workoutExercises = ref([]);

const exerciseDrafts = ref({});
const setDrafts = ref({});
const setsByWorkoutExercise = ref({});

const newTemplate = ref({ day_of_week: 1, label: "" });
const addTemplateExerciseDraft = ref({ exercise_id: "", order: "" });
const newWorkoutDraft = ref({ date: new Date().toISOString().slice(0, 10), duration: "" });
const addWorkoutExerciseDraft = ref({ exercise_id: "", order: "", notes: "" });

const dayNames = {
  1: "Monday",
  2: "Tuesday",
  3: "Wednesday",
  4: "Thursday",
  5: "Friday",
  6: "Saturday",
  7: "Sunday"
};

const selectedProgram = computed(() =>
  programs.value.find((program) => program.id === Number(selectedProgramId.value)) || null
);

const selectedTemplate = computed(() =>
  templates.value.find((template) => template.id === Number(selectedTemplateId.value)) || null
);

const exerciseNameById = (exerciseId) => {
  const match = exercises.value.find((item) => item.id === exerciseId);
  return match ? match.name : `Exercise #${exerciseId}`;
};

const sortedTemplateExercises = computed(() =>
  [...templateExercises.value].sort((a, b) => a.order - b.order)
);

const sortedWorkoutExercises = computed(() =>
  [...workoutExercises.value].sort((a, b) => a.order - b.order)
);

watch(selectedProgramId, async (next) => {
  if (!next) {
    return;
  }

  await loadProgramData(Number(next));
});

watch(selectedTemplateId, async (next) => {
  if (!next) {
    templateExercises.value = [];
    return;
  }

  await loadTemplateExercises(Number(next));
});

watch(selectedWorkoutId, async (next) => {
  if (!next) {
    selectedWorkout.value = null;
    workoutExercises.value = [];
    return;
  }

  await loadWorkoutDetails(Number(next));
});

async function withUiState(callback) {
  try {
    error.value = "";
    await callback();
  } catch (err) {
    error.value = err.message || "Unexpected API error";
  }
}

async function loadBootstrap() {
  loading.value = true;
  await withUiState(async () => {
    const [programResult, exerciseResult] = await Promise.all([
      api.getPrograms(),
      api.getExercises()
    ]);

    programs.value = programResult;
    exercises.value = exerciseResult;

    if (programs.value.length > 0) {
      selectedProgramId.value = programs.value[0].id;
      await loadProgramData(programs.value[0].id);
    }
  });
  loading.value = false;
}

async function loadProgramData(programId) {
  loading.value = true;
  await withUiState(async () => {
    const [templateResult, workoutResult] = await Promise.all([
      api.getProgramTemplates(programId),
      api.getProgramWorkouts(programId)
    ]);

    templates.value = templateResult.sort((a, b) => a.day_of_week - b.day_of_week);
    workouts.value = workoutResult.sort((a, b) => (a.date < b.date ? 1 : -1));

    if (templates.value.length > 0) {
      if (!templates.value.some((template) => template.id === Number(selectedTemplateId.value))) {
        selectedTemplateId.value = templates.value[0].id;
      }
      await loadTemplateExercises(Number(selectedTemplateId.value));
    } else {
      selectedTemplateId.value = null;
      templateExercises.value = [];
    }

    if (workouts.value.length > 0) {
      if (!workouts.value.some((workout) => workout.id === Number(selectedWorkoutId.value))) {
        selectedWorkoutId.value = workouts.value[0].id;
      }
      await loadWorkoutDetails(Number(selectedWorkoutId.value));
    } else {
      selectedWorkoutId.value = null;
      selectedWorkout.value = null;
      workoutExercises.value = [];
      setsByWorkoutExercise.value = {};
    }
  });
  loading.value = false;
}

async function loadTemplateExercises(templateId) {
  await withUiState(async () => {
    templateExercises.value = await api.getTemplateExercises(templateId);
  });
}

function initExerciseDrafts(items) {
  const nextDrafts = {};
  items.forEach((item) => {
    nextDrafts[item.id] = {
      order: item.order,
      notes: item.notes || "",
      exercise_id: item.exercise_id
    };

    if (!setDrafts.value[item.id]) {
      setDrafts.value[item.id] = { set_number: "", weight: "", reps: "" };
    }
  });
  exerciseDrafts.value = nextDrafts;
}

async function loadWorkoutDetails(workoutId) {
  loading.value = true;
  await withUiState(async () => {
    const [workoutResult, workoutExerciseResult] = await Promise.all([
      api.getWorkout(workoutId),
      api.getWorkoutExercises(workoutId)
    ]);

    selectedWorkout.value = workoutResult;
    workoutExercises.value = workoutExerciseResult;
    initExerciseDrafts(workoutExerciseResult);

    const setPairs = await Promise.all(
      workoutExerciseResult.map(async (workoutExercise) => [
        workoutExercise.id,
        await api.getWorkoutExerciseSets(workoutExercise.id)
      ])
    );

    const nextSets = {};
    setPairs.forEach(([workoutExerciseId, sets]) => {
      nextSets[workoutExerciseId] = sets.sort((a, b) => a.set_number - b.set_number);
    });
    setsByWorkoutExercise.value = nextSets;
  });
  loading.value = false;
}

async function createTemplate() {
  if (!selectedProgramId.value) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.createTemplate(Number(selectedProgramId.value), {
      day_of_week: Number(newTemplate.value.day_of_week),
      label: newTemplate.value.label || null,
      program_id: Number(selectedProgramId.value)
    });

    newTemplate.value = { day_of_week: 1, label: "" };
    await loadProgramData(Number(selectedProgramId.value));
  });
  saving.value = false;
}

async function addTemplateExercise() {
  if (!selectedTemplateId.value || !addTemplateExerciseDraft.value.exercise_id) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.addTemplateExercise(Number(selectedTemplateId.value), {
      workout_template_id: Number(selectedTemplateId.value),
      exercise_id: Number(addTemplateExerciseDraft.value.exercise_id),
      order: addTemplateExerciseDraft.value.order
        ? Number(addTemplateExerciseDraft.value.order)
        : null
    });

    addTemplateExerciseDraft.value = { exercise_id: "", order: "" };
    await loadTemplateExercises(Number(selectedTemplateId.value));
  });
  saving.value = false;
}

async function moveTemplateExercise(item, direction) {
  const nextOrder = item.order + direction;
  if (nextOrder < 1 || nextOrder > templateExercises.value.length) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.moveTemplateExercise(item.id, nextOrder);
    await loadTemplateExercises(Number(selectedTemplateId.value));
  });
  saving.value = false;
}

async function deleteTemplateExercise(templateExerciseId) {
  saving.value = true;
  await withUiState(async () => {
    await api.deleteTemplateExercise(templateExerciseId);
    await loadTemplateExercises(Number(selectedTemplateId.value));
  });
  saving.value = false;
}

async function createWorkoutFromTemplate() {
  if (!selectedTemplateId.value || !selectedProgramId.value) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.createWorkoutFromTemplate(Number(selectedTemplateId.value), {
      program_id: Number(selectedProgramId.value),
      template_id: Number(selectedTemplateId.value),
      date: newWorkoutDraft.value.date,
      duration: newWorkoutDraft.value.duration ? Number(newWorkoutDraft.value.duration) : null
    });

    newWorkoutDraft.value = { date: new Date().toISOString().slice(0, 10), duration: "" };
    await loadProgramData(Number(selectedProgramId.value));
  });
  saving.value = false;
}

async function addWorkoutExercise() {
  if (!selectedWorkoutId.value || !addWorkoutExerciseDraft.value.exercise_id) {
    return;
  }

  const fallbackOrder = sortedWorkoutExercises.value.length + 1;

  saving.value = true;
  await withUiState(async () => {
    await api.addWorkoutExercise(Number(selectedWorkoutId.value), {
      order: addWorkoutExerciseDraft.value.order ? Number(addWorkoutExerciseDraft.value.order) : fallbackOrder,
      notes: addWorkoutExerciseDraft.value.notes || "",
      workout_id: Number(selectedWorkoutId.value),
      exercise_id: Number(addWorkoutExerciseDraft.value.exercise_id)
    });

    addWorkoutExerciseDraft.value = { exercise_id: "", order: "", notes: "" };
    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

async function saveWorkoutExercise(workoutExerciseId) {
  const draft = exerciseDrafts.value[workoutExerciseId];
  if (!draft || !selectedWorkoutId.value) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.updateWorkoutExercise(workoutExerciseId, {
      id: workoutExerciseId,
      order: Number(draft.order),
      notes: draft.notes || "",
      workout_id: Number(selectedWorkoutId.value),
      exercise_id: Number(draft.exercise_id)
    });

    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

async function deleteWorkoutExercise(workoutExerciseId) {
  if (!selectedWorkoutId.value) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.deleteWorkoutExercise(workoutExerciseId);
    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

async function addSet(workoutExerciseId) {
  if (!selectedWorkoutId.value) {
    return;
  }

  const draft = setDrafts.value[workoutExerciseId];
  if (!draft || !draft.set_number || !draft.weight || !draft.reps) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.addWorkoutExerciseSet(workoutExerciseId, {
      set_number: Number(draft.set_number),
      weight: Number(draft.weight),
      reps: Number(draft.reps),
      workout_exercise_id: workoutExerciseId
    });

    setDrafts.value[workoutExerciseId] = { set_number: "", weight: "", reps: "" };
    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

async function saveSet(workoutExerciseId, setItem) {
  saving.value = true;
  await withUiState(async () => {
    await api.updateSet(setItem.id, {
      id: setItem.id,
      set_number: Number(setItem.set_number),
      weight: Number(setItem.weight),
      reps: Number(setItem.reps),
      workout_exercise_id: workoutExerciseId
    });

    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

async function deleteSet(setId) {
  if (!selectedWorkoutId.value) {
    return;
  }

  saving.value = true;
  await withUiState(async () => {
    await api.deleteSet(setId);
    await loadWorkoutDetails(Number(selectedWorkoutId.value));
  });
  saving.value = false;
}

onMounted(loadBootstrap);
</script>

<template>
  <main class="app-shell">
    <header class="hero">
      <h1>ExerciseDB Training Console</h1>
      <p>Phase 1: build templates and log workouts.</p>
    </header>

    <section class="panel top-controls">
      <label>
        Program
        <select v-model="selectedProgramId">
          <option v-for="program in programs" :key="program.id" :value="program.id">
            {{ program.name }}
          </option>
        </select>
      </label>
      <button class="ghost" @click="loadProgramData(Number(selectedProgramId))" :disabled="!selectedProgramId">
        Refresh Program Data
      </button>
      <span v-if="loading">Loading...</span>
      <span v-if="saving">Saving...</span>
      <span v-if="error" class="error">{{ error }}</span>
    </section>

    <section class="layout-grid">
      <article class="panel">
        <h2>Template Builder</h2>

        <form class="inline-grid" @submit.prevent="createTemplate">
          <label>
            Day
            <select v-model="newTemplate.day_of_week">
              <option v-for="(dayName, dayNumber) in dayNames" :key="dayNumber" :value="Number(dayNumber)">
                {{ dayName }}
              </option>
            </select>
          </label>
          <label>
            Label
            <input v-model="newTemplate.label" placeholder="Lower body A" />
          </label>
          <button type="submit" :disabled="!selectedProgramId">Create Template</button>
        </form>

        <label>
          Select Template
          <select v-model="selectedTemplateId">
            <option v-for="template in templates" :key="template.id" :value="template.id">
              #{{ template.id }} - {{ dayNames[template.day_of_week] }}{{ template.label ? ` (${template.label})` : "" }}
            </option>
          </select>
        </label>

        <form class="inline-grid" @submit.prevent="addTemplateExercise">
          <label>
            Exercise
            <select v-model="addTemplateExerciseDraft.exercise_id">
              <option value="">Select</option>
              <option v-for="exercise in exercises" :key="exercise.id" :value="exercise.id">
                {{ exercise.name }}
              </option>
            </select>
          </label>
          <label>
            Order (optional)
            <input v-model="addTemplateExerciseDraft.order" type="number" min="1" />
          </label>
          <button type="submit" :disabled="!selectedTemplateId">Add Template Exercise</button>
        </form>

        <ul class="stack-list">
          <li v-for="item in sortedTemplateExercises" :key="item.id" class="list-item">
            <div>
              <strong>{{ item.order }}.</strong> {{ exerciseNameById(item.exercise_id) }}
            </div>
            <div class="button-row">
              <button class="ghost" @click="moveTemplateExercise(item, -1)">Up</button>
              <button class="ghost" @click="moveTemplateExercise(item, 1)">Down</button>
              <button class="danger" @click="deleteTemplateExercise(item.id)">Remove</button>
            </div>
          </li>
        </ul>

        <form class="inline-grid" @submit.prevent="createWorkoutFromTemplate">
          <h3>Start Workout From Template</h3>
          <label>
            Date
            <input v-model="newWorkoutDraft.date" type="date" required />
          </label>
          <label>
            Duration (minutes)
            <input v-model="newWorkoutDraft.duration" type="number" min="1" />
          </label>
          <button type="submit" :disabled="!selectedTemplateId">Create Workout Log</button>
        </form>
      </article>

      <article class="panel">
        <h2>Workout Logging</h2>

        <label>
          Select Workout
          <select v-model="selectedWorkoutId">
            <option v-for="workout in workouts" :key="workout.id" :value="workout.id">
              #{{ workout.id }} - {{ workout.date }}
            </option>
          </select>
        </label>

        <p v-if="selectedWorkout">
          Workout #{{ selectedWorkout.id }} | Template #{{ selectedWorkout.template_id }} | Date {{ selectedWorkout.date }}
        </p>

        <form class="inline-grid" @submit.prevent="addWorkoutExercise">
          <label>
            Add Exercise
            <select v-model="addWorkoutExerciseDraft.exercise_id">
              <option value="">Select</option>
              <option v-for="exercise in exercises" :key="exercise.id" :value="exercise.id">
                {{ exercise.name }}
              </option>
            </select>
          </label>
          <label>
            Order
            <input v-model="addWorkoutExerciseDraft.order" type="number" min="1" placeholder="Auto = end" />
          </label>
          <label>
            Notes
            <input v-model="addWorkoutExerciseDraft.notes" placeholder="Optional notes" />
          </label>
          <button type="submit" :disabled="!selectedWorkoutId">Add Workout Exercise</button>
        </form>

        <div v-for="workoutExercise in sortedWorkoutExercises" :key="workoutExercise.id" class="exercise-card">
          <header class="exercise-head">
            <h3>{{ workoutExercise.order }}. {{ exerciseNameById(workoutExercise.exercise_id) }}</h3>
            <button class="danger" @click="deleteWorkoutExercise(workoutExercise.id)">Delete Exercise</button>
          </header>

          <div class="inline-grid">
            <label>
              Exercise
              <select v-model="exerciseDrafts[workoutExercise.id].exercise_id">
                <option v-for="exercise in exercises" :key="exercise.id" :value="exercise.id">
                  {{ exercise.name }}
                </option>
              </select>
            </label>
            <label>
              Order
              <input v-model="exerciseDrafts[workoutExercise.id].order" type="number" min="1" />
            </label>
            <label>
              Notes
              <input v-model="exerciseDrafts[workoutExercise.id].notes" />
            </label>
            <button @click="saveWorkoutExercise(workoutExercise.id)">Save Exercise Changes</button>
          </div>

          <h4>Sets</h4>
          <table class="set-table" v-if="setsByWorkoutExercise[workoutExercise.id]?.length">
            <thead>
              <tr>
                <th>#</th>
                <th>Weight</th>
                <th>Reps</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="setItem in setsByWorkoutExercise[workoutExercise.id]" :key="setItem.id">
                <td><input v-model="setItem.set_number" type="number" min="1" /></td>
                <td><input v-model="setItem.weight" type="number" min="0" /></td>
                <td><input v-model="setItem.reps" type="number" min="0" /></td>
                <td class="button-row">
                  <button class="ghost" @click="saveSet(workoutExercise.id, setItem)">Save</button>
                  <button class="danger" @click="deleteSet(setItem.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else>No sets yet.</p>

          <form class="set-form" @submit.prevent="addSet(workoutExercise.id)">
            <input v-model="setDrafts[workoutExercise.id].set_number" type="number" min="1" placeholder="Set #" />
            <input v-model="setDrafts[workoutExercise.id].weight" type="number" min="0" placeholder="Weight" />
            <input v-model="setDrafts[workoutExercise.id].reps" type="number" min="0" placeholder="Reps" />
            <button type="submit">Add Set</button>
          </form>
        </div>
      </article>
    </section>
  </main>
</template>

<style scoped>
:global(body) {
  margin: 0;
  font-family: "Avenir Next", "Segoe UI", "Trebuchet MS", sans-serif;
  background: radial-gradient(circle at top left, #ffe9d1 0%, #f8f4ef 35%, #d5dce6 100%);
  color: #1a1f2b;
}

.app-shell {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
}

.hero {
  margin-bottom: 1rem;
  padding: 1.2rem;
  border-radius: 14px;
  background: linear-gradient(120deg, #173753, #287271);
  color: #f9fafb;
}

.hero h1 {
  margin: 0;
  letter-spacing: 0.02em;
}

.hero p {
  margin: 0.5rem 0 0;
}

.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 1rem;
}

.panel {
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(23, 55, 83, 0.16);
  backdrop-filter: blur(8px);
  padding: 1rem;
}

.top-controls {
  margin-bottom: 1rem;
  display: flex;
  gap: 0.75rem;
  align-items: end;
  flex-wrap: wrap;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-size: 0.92rem;
}

input,
select,
button {
  border-radius: 10px;
  border: 1px solid #9db4c8;
  padding: 0.45rem 0.55rem;
  font-size: 0.92rem;
}

button {
  background: #287271;
  color: #fff;
  border-color: #287271;
  cursor: pointer;
}

button:hover {
  filter: brightness(1.08);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button.ghost {
  background: #e9f2f8;
  color: #173753;
  border-color: #87a9c6;
}

button.danger {
  background: #d3423f;
  border-color: #d3423f;
}

.inline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 0.6rem;
  margin: 0.8rem 0;
}

.stack-list {
  list-style: none;
  padding: 0;
  margin: 0.6rem 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
  border-bottom: 1px solid #d6dee8;
  padding: 0.45rem 0;
}

.button-row {
  display: flex;
  gap: 0.35rem;
}

.exercise-card {
  border: 1px solid #d3dde8;
  border-radius: 12px;
  padding: 0.7rem;
  margin-top: 0.8rem;
  background: #fbfdff;
}

.exercise-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.exercise-head h3 {
  margin: 0;
  font-size: 1rem;
}

.set-table {
  width: 100%;
  border-collapse: collapse;
}

.set-table th,
.set-table td {
  border-bottom: 1px solid #d4dde9;
  padding: 0.35rem;
  text-align: left;
}

.set-form {
  margin-top: 0.6rem;
  display: grid;
  grid-template-columns: repeat(4, minmax(80px, 1fr));
  gap: 0.5rem;
}

.error {
  color: #9d1b18;
  font-weight: 600;
}

@media (max-width: 700px) {
  .app-shell {
    padding: 1rem;
  }

  .set-form {
    grid-template-columns: 1fr;
  }
}
</style>
