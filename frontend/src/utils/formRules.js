// TODO:国际化
export default {
  no: [
    {
      required: true,
      message: 'Please input no',
      trigger: 'blur'
    },
    {
      pattern: '^d{3,}$',
      message: 'Please input correct no'
    }
  ],
  addNo: [
    {
      required: true,
      message: 'Please input no',
      trigger: 'blur'
    },
    { min: 7, max: 7, message: 'Length should be 7', trigger: 'blur' }
  ],
  name: [
    { required: true, message: 'Please input name', trigger: 'blur' },
    { min: 2, max: 16, message: 'Length should be 2 to 16', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 3, max: 16, message: 'Length should be 3 to 16', trigger: 'blur' }
  ],
  gender: [{ required: true, message: 'Please input gender', trigger: 'blur' }],
  email: [
    {
      type: 'email',
      message: 'Please input correct email address',
      trigger: ['blur', 'change']
    }
  ],
  tel: [
    {
      pattern: '^[0-9]+(-[0-9]+)*$',
      message: 'Please input correct telephone number'
    }
  ],
  major: [{ required: true, message: 'Please input major', trigger: 'blur' }],
  grade: [
    {
      pattern: '^[0-9]+$',
      message: 'Please input numbers'
    },
    { min: 4, max: 4, message: 'Length should be 4', trigger: 'blur' }
  ],
  classno: [{ type: 'number', message: 'class must be a number' }],
  vericode: [
    {
      required: true,
      message: 'Please input verification code',
      trigger: 'blur'
    },
    { min: 6, max: 6, message: 'Length should be 6', trigger: 'blur' }
  ]
}
