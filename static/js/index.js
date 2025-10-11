window.app = Vue.createApp({
  el: '#vue',
  mixins: [windowMixin],
  delimiters: ['${', '}'],
  data: function () {
    return {
      currencyOptions: ['sat'],
      settingsFormDialog: {
        show: false,
        data: {}
      },

      scrumFormDialog: {
        show: false,
        data: {
          name: null,
          description: null,
          public_assigning: false
        }
      },
      scrumList: [],
      scrumTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'name',
            align: 'left',
            label: 'Scrum Name',
            field: 'name',
            sortable: true
          },
          {
            name: 'description',
            align: 'left',
            label: 'Scrum Description',
            field: 'description',
            sortable: true
          },
          {
            name: 'updated_at',
            align: 'left',
            label: 'Updated At',
            field: 'updated_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      },

      tasksFormDialog: {
        show: false,
        scrum: {label: 'All Scrum', value: ''},
        data: {
          complete: false
        }
      },
      tasksList: [],
      tasksTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'task',
            align: 'left',
            label: 'Task',
            field: 'task',
            sortable: true
          },
          {
            name: 'assignee',
            align: 'left',
            label: 'assignee',
            field: 'assignee',
            sortable: true
          },
          {
            name: 'stage',
            align: 'left',
            label: 'Stage',
            field: 'stage',
            sortable: true
          },
          {
            name: 'reward',
            align: 'left',
            label: 'Reward',
            field: 'reward',
            sortable: true
          },
          {
            name: 'complete',
            align: 'left',
            label: 'Complete',
            field: 'complete',
            sortable: true
          },
          {
            name: 'paid',
            align: 'left',
            label: 'Paid',
            field: 'paid',
            sortable: true
          },
          {
            name: 'notes',
            align: 'left',
            label: 'Notes',
            field: 'notes',
            sortable: true
          },
          {
            name: 'updated_at',
            align: 'left',
            label: 'Updated At',
            field: 'updated_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      }
    }
  },
  watch: {
    'scrumTable.search': {
      handler() {
        const props = {}
        if (this.scrumTable.search) {
          props['search'] = this.scrumTable.search
        }
        this.getScrum()
      }
    },
    'tasksTable.search': {
      handler() {
        const props = {}
        if (this.tasksTable.search) {
          props['search'] = this.tasksTable.search
        }
        this.getTasks()
      }
    },
    'tasksFormDialog.scrum.value': {
      handler() {
        const props = {}
        if (this.tasksTable.search) {
          props['search'] = this.tasksTable.search
        }
        this.getTasks()
      }
    }
  },

  methods: {
    //////////////// Scrum ////////////////////////
    async showNewScrumForm() {
      this.scrumFormDialog.data = {
        name: null,
        description: null,
        public_assigning: false
      }
      this.scrumFormDialog.show = true
    },
    async showEditScrumForm(data) {
      this.scrumFormDialog.data = {...data}
      this.scrumFormDialog.show = true
    },
    async saveScrum() {
      try {
        const data = {extra: {}, ...this.scrumFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/scrum/api/v1/scrum' + entry,
          null,
          data
        )
        this.getScrum()
        this.scrumFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getScrum(props) {
      try {
        this.scrumTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(this.scrumTable, props)
        const {data} = await LNbits.api.request(
          'GET',
          `/scrum/api/v1/scrum/paginated?${params}`,
          null
        )
        this.scrumList = data.data
        this.scrumTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.scrumTable.loading = false
      }
    },
    async deleteScrum(scrumId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Scrum?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/scrum/api/v1/scrum/' + scrumId,
              null
            )
            await this.getScrum()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },
    async exportScrumCSV() {
      await LNbits.utils.exportCSV(
        this.scrumTable.columns,
        this.scrumList,
        'scrum_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Tasks ////////////////////////
    async showEditTasksForm(data) {
      if (data) {
        this.tasksFormDialog.data = {...data}
      }
      this.tasksFormDialog.show = true
    },
    async saveTasks() {
      try {
        const data = {extra: {}, ...this.tasksFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/scrum/api/v1/tasks' + entry,
          null,
          data
        )
        this.getTasks()
        this.tasksFormDialog.show = false
        this.tasksFormDialog.data = {}
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    clearForm() {
      this.tasksFormDialog.show = false
      this.tasksFormDialog.data = {}
      this.scrumFormDialog.show = false
      this.scrumFormDialog.data = {}
    },
    async getTasks(props) {
      try {
        this.tasksTable.loading = true
        let params = LNbits.utils.prepareFilterQuery(this.tasksTable, props)
        const scrumId = this.tasksFormDialog.scrum.value
        if (scrumId) {
          params += `&scrum_id=${scrumId}`
        }
        const {data} = await LNbits.api.request(
          'GET',
          `/scrum/api/v1/tasks/paginated?${params}`,
          null
        )
        this.tasksList = data.data
        this.tasksTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.tasksTable.loading = false
      }
    },
    async deleteTasks(tasksId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Tasks?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/scrum/api/v1/tasks/' + tasksId,
              null
            )
            await this.getTasks()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },

    async exportTasksCSV() {
      await LNbits.utils.exportCSV(
        this.tasksTable.columns,
        this.tasksList,
        'tasks_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow()
    },
    async fetchCurrencies() {
      try {
        const response = await LNbits.api.request('GET', '/api/v1/currencies')
        this.currencyOptions = ['sat', ...response.data]
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    }
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.fetchCurrencies()
    this.getScrum()
    this.getTasks()
  }
})
