const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const config = {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  };

  if (!config.body) {
    delete config.headers["Content-Type"];
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API ${response.status}: ${message || response.statusText}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  getPrograms: () => request("/programs"),
  createProgram: (payload) => request("/programs", { method: "POST", body: JSON.stringify(payload) }),
  getExercises: () => request("/exercises?limit=100"),
  getProgramTemplates: (programId) => request(`/programs/${programId}/templates`),
  createTemplate: (programId, payload) => request(`/programs/${programId}/templates`, { method: "POST", body: JSON.stringify(payload) }),
  getTemplateExercises: (templateId) => request(`/workout_templates/${templateId}/exercises`),
  addTemplateExercise: (templateId, payload) => request(`/workout_templates/${templateId}/template_exercises`, { method: "POST", body: JSON.stringify(payload) }),
  moveTemplateExercise: (templateExerciseId, order) => request(`/template_exercises/${templateExerciseId}?order=${order}`, { method: "PUT" }),
  deleteTemplateExercise: (templateExerciseId) => request(`/template_exercises/${templateExerciseId}`, { method: "DELETE" }),
  createWorkoutFromTemplate: (templateId, payload) => request(`/workout_templates/${templateId}/workouts`, { method: "POST", body: JSON.stringify(payload) }),
  getProgramWorkouts: (programId) => request(`/programs/${programId}/workouts`),
  getWorkout: (workoutId) => request(`/workouts/${workoutId}`),
  getWorkoutExercises: (workoutId) => request(`/workouts/${workoutId}/exercises`),
  addWorkoutExercise: (workoutId, payload) => request(`/workouts/${workoutId}/workout_exercises`, { method: "POST", body: JSON.stringify(payload) }),
  updateWorkoutExercise: (workoutExerciseId, payload) => request(`/workout_exercises/${workoutExerciseId}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteWorkoutExercise: (workoutExerciseId) => request(`/workout_exercises/${workoutExerciseId}`, { method: "DELETE" }),
  getWorkoutExerciseSets: (workoutExerciseId) => request(`/workout_exercises/${workoutExerciseId}/exercise_sets`),
  addWorkoutExerciseSet: (workoutExerciseId, payload) => request(`/workout_exercises/${workoutExerciseId}/exercise_sets`, { method: "POST", body: JSON.stringify(payload) }),
  updateSet: (setId, payload) => request(`/exercise_sets/${setId}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteSet: (setId) => request(`/exercise_sets/${setId}`, { method: "DELETE" })
};
