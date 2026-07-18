{{- define "gitops-app.fullname" -}}
{{- printf "%s-%s" .Values.student.prenom .Values.student.nom | lower | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "gitops-app.labels" -}}
app.kubernetes.io/name: {{ include "gitops-app.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
student: {{ .Values.student.prenom | lower }}-{{ .Values.student.nom | lower }}
{{- end -}}
