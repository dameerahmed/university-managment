import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Sidebar from '../components/Sidebar';
import { Search, Filter, ChevronDown, User, BookOpen, Layers, Plus, Edit, Trash2 } from 'lucide-react';
import StudentModal from '../components/StudentModal';

const ManageStudents = () => {
  // --- 1. DATA HOLDING STATES ---
  const [students, setStudents] = useState([]); // Raw data from API
  const [tableData, setTableData] = useState([]); // Filtered data for table
  const [departments, setDepartments] = useState([]);
  const [batches, setBatches] = useState([]);
  const [rollNumbers, setRollNumbers] = useState([]);
  const [loading, setLoading] = useState(false);

  // --- 2. FILTER STATES ---
  const [selectedDept, setSelectedDept] = useState('');
  const [selectedBatch, setSelectedBatch] = useState('');
  const [selectedStudent, setSelectedStudent] = useState(''); // Stores roll_number

  // --- 3. PAGINATION STATES ---
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 8;

  // --- 4. MODAL STATES ---
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);

  // --- 5. INITIAL DATA FETCHING ---
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const deptRes = await api.get('/departments/dropdown');
        setDepartments(deptRes.data);
      } catch (err) {
        console.error("Failed to fetch initial data:", err);
      }
    };
    fetchInitialData();
  }, []);

  // Fetch Batches when Department changes
  useEffect(() => {
    const fetchBatches = async () => {
      if (!selectedDept) {
        setBatches([]);
        setSelectedBatch('');
        return;
      }
      try {
        const response = await api.get('/batches/dropdown', {
          params: { department_id: selectedDept }
        });
        setBatches(response.data);
        setSelectedBatch(''); // Reset batch selection
      } catch (err) {
        console.error("Failed to fetch batches:", err);
      }
    };
    fetchBatches();
  }, [selectedDept]);

  // Fetch Students (Roll Numbers) when Batch changes
  useEffect(() => {
    const fetchRollNumbers = async () => {
      if (!selectedDept || !selectedBatch) {
        setRollNumbers([]);
        return;
      }
      try {
        const response = await api.get('/students/class_roll_numbers', {
          params: { department_id: selectedDept, batch_id: selectedBatch }
        });
        setRollNumbers(response.data);
      } catch (err) {
        console.error("Failed to fetch roll numbers:", err);
      }
    };
    fetchRollNumbers();
  }, [selectedDept, selectedBatch]);


  const handleCreate = () => {
    setEditingStudent(null);
    setIsModalOpen(true);
  };

  const handleEdit = (student) => {
    setEditingStudent(student);
    setIsModalOpen(true);
  };

  const handleDelete = async (rollNumber) => {
    if (!window.confirm("Are you sure you want to delete this student?")) return;
    try {
      await api.delete(`/students/delete/${rollNumber}`);
      // Refresh table if the deleted student was in the current view
      if (tableData.find(s => s.roll_number === rollNumber)) {
        handleSearch();
      }
      alert("Student deleted successfully");
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to delete student");
    }
  };

  const handleModalSubmit = async (formData) => {
    try {
      if (editingStudent) {
        await api.put(`/students/update/${editingStudent.roll_number}`, formData);
        alert("Student updated successfully");
      } else {
        await api.post('/students/create', formData);
        alert("Student created successfully");
      }
      // Refresh data
      if (selectedDept && selectedBatch) {
        handleSearch();
      }
    } catch (err) {
      console.error("Operation failed:", err);
      throw new Error(err.response?.data?.detail || "Operation failed");
    }
  };

  // --- 6. MAIN SEARCH BUTTON LOGIC ---
  const handleSearch = async () => {
    if (!selectedDept || !selectedBatch) {
      alert("Please select both Department and Batch.");
      return;
    }

    setLoading(true);
    setCurrentPage(1); // Reset to first page on new search
    try {
      const response = await api.get('/students/', {
        params: {
          department_id: selectedDept,
          batch_id: selectedBatch,
          roll_number: selectedStudent || null
        }
      });
      setTableData(response.data);
    } catch (err) {
      console.error("Search Failed:", err);
    } finally {
      setLoading(false);
    }
  };

  // --- 7. PAGINATION LOGIC ---
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = tableData.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(tableData.length / itemsPerPage);

  const nextPage = () => {
    if (currentPage < totalPages) setCurrentPage(prev => prev + 1);
  };

  const prevPage = () => {
    if (currentPage > 1) setCurrentPage(prev => prev - 1);
  };

  return (
    <div className="flex min-h-screen bg-dark-900 font-sans text-gray-300 selection:bg-accent-purple selection:text-white">
      <Sidebar />

      <div className="flex-1 p-8 overflow-y-auto w-full relative">
        {/* Background Gradients */}
        <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
          <div className="absolute top-[10%] right-[20%] w-[400px] h-[400px] bg-accent-blue/10 rounded-full blur-[120px]"></div>
        </div>

        <div className="relative z-10">
          {/* HEADER SECTION */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
            <div>
              <h1 className="text-3xl font-bold text-white tracking-tight">
                Manage Students
              </h1>
              <p className="text-gray-400 mt-1">Manage and search student profiles with ease.</p>
            </div>
            <div className="hidden md:block">
              <button
                onClick={handleCreate}
                className="bg-accent-purple hover:bg-accent-purple/90 text-white font-bold py-3 px-6 rounded-xl shadow-[0_0_20px_rgba(139,92,246,0.3)] transition-all flex items-center gap-2 transform hover:-translate-y-0.5 active:scale-95"
              >
                <Plus size={20} /> Add Student
              </button>
            </div>
          </div>

          {/* SEARCH & FILTER BAR */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-3xl shadow-2xl mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-100">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">

              {/* Department Dropdown */}
              <div className="relative group">
                <label className="block text-xs font-bold text-gray-400 mb-2 ml-1 uppercase tracking-wider">Department</label>
                <div className="relative">
                  <Layers className="absolute left-4 top-1/2 transform -translate-y-1/2 text-accent-purple" size={18} />
                  <select
                    className="w-full pl-11 pr-10 py-3 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none appearance-none text-gray-200 font-medium cursor-pointer hover:bg-dark-800"
                    value={selectedDept}
                    onChange={(e) => setSelectedDept(e.target.value)}
                  >
                    <option value="">Select Dept</option>
                    {departments.map(dept => (
                      <option key={dept.department_id} value={dept.department_id}>{dept.department_name}</option>
                    ))}
                  </select>
                  <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none" size={16} />
                </div>
              </div>

              {/* Batch Dropdown */}
              <div className="relative group">
                <label className="block text-xs font-bold text-gray-400 mb-2 ml-1 uppercase tracking-wider">Batch</label>
                <div className="relative">
                  <BookOpen className="absolute left-4 top-1/2 transform -translate-y-1/2 text-accent-purple" size={18} />
                  <select
                    className="w-full pl-11 pr-10 py-3 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none appearance-none text-gray-200 font-medium cursor-pointer hover:bg-dark-800 disabled:opacity-50 disabled:cursor-not-allowed"
                    value={selectedBatch}
                    onChange={(e) => setSelectedBatch(e.target.value)}
                    disabled={!selectedDept}
                  >
                    <option value="">Select Batch</option>
                    {batches.map(batch => (
                      <option key={batch.batch_id} value={batch.batch_id}>{batch.batch_name}</option>
                    ))}
                  </select>
                  <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none" size={16} />
                </div>
              </div>

              {/* Student Dropdown */}
              <div className="relative group">
                <label className="block text-xs font-bold text-gray-400 mb-2 ml-1 uppercase tracking-wider">Student (Optional)</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 transform -translate-y-1/2 text-accent-purple" size={18} />
                  <select
                    className="w-full pl-11 pr-10 py-3 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none appearance-none text-gray-200 font-medium cursor-pointer hover:bg-dark-800 disabled:opacity-50 disabled:cursor-not-allowed"
                    value={selectedStudent}
                    onChange={(e) => setSelectedStudent(e.target.value)}
                    disabled={!selectedBatch}
                  >
                    <option value="">All Students</option>
                    {rollNumbers.length === 0 && selectedBatch ? (
                      <option disabled>No students found</option>
                    ) : (
                      rollNumbers.map(roll => (
                        <option key={roll} value={roll}>{roll}</option>
                      ))
                    )}
                  </select>
                  <ChevronDown className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none" size={16} />
                </div>
              </div>

              {/* Search Button */}
              <button
                onClick={handleSearch}
                className="w-full bg-white/10 hover:bg-white/20 border border-white/10 text-white font-bold py-3 rounded-xl transition-all flex items-center justify-center gap-2 transform hover:-translate-y-0.5 active:scale-95 h-[50px]"
              >
                <Search size={20} /> Search
              </button>

            </div>
          </div>

          {/* TABLE SECTION */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-500 delay-200 shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-white/5 border-b border-white/5">
                  <tr>
                    <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Student Name</th>
                    <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Roll Number</th>
                    <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Department</th>
                    <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Status</th>
                    <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {loading ? (
                    <tr>
                      <td colSpan="5" className="text-center py-12">
                        <div className="flex justify-center items-center gap-3 text-gray-400">
                          <div className="w-5 h-5 border-2 border-accent-purple border-t-transparent rounded-full animate-spin"></div>
                          Fetching student data...
                        </div>
                      </td>
                    </tr>
                  ) : tableData.length === 0 ? (
                    <tr>
                      <td colSpan="5" className="text-center py-16">
                        <div className="flex flex-col items-center gap-3 text-gray-500">
                          <div className="p-4 bg-white/5 rounded-full">
                            <User size={32} className="text-gray-600" />
                          </div>
                          <p className="font-medium text-sm">No students found. Try adjusting your filters.</p>
                        </div>
                      </td>
                    </tr>
                  ) : (
                    currentItems.map((student, index) => (
                      <tr key={student.student_id} className="hover:bg-white/5 transition-colors group">
                        <td className="px-8 py-4 whitespace-nowrap">
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-purple/20 to-accent-blue/20 text-accent-purple flex items-center justify-center font-bold text-lg border border-white/10">
                              {student.first_name?.[0] || '?'}
                            </div>
                            <div>
                              <div className="font-bold text-gray-200 group-hover:text-white transition-colors">{student.first_name} {student.last_name}</div>
                              <div className="text-xs text-gray-500 font-medium">{student.email}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-8 py-4 whitespace-nowrap">
                          <span className="font-mono text-xs font-bold text-accent-blue bg-accent-blue/10 border border-accent-blue/20 px-2 py-1 rounded-lg">
                            {student.roll_number}
                          </span>
                        </td>
                        <td className="px-8 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-300">{student.department?.department_name || 'N/A'}</div>
                          <div className="text-[10px] text-gray-500 uppercase tracking-wider font-bold mt-0.5">Batch {selectedBatch}</div>
                        </td>
                        <td className="px-8 py-4 whitespace-nowrap">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wide">
                            Active
                          </span>
                        </td>
                        <td className="px-8 py-4 whitespace-nowrap">
                          <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={() => handleEdit(student)}
                              className="text-gray-400 hover:text-accent-purple transition-colors p-2 hover:bg-accent-purple/10 rounded-lg"
                              title="Edit Student"
                            >
                              <Edit size={16} />
                            </button>
                            <button
                              onClick={() => handleDelete(student.roll_number)}
                              className="text-gray-400 hover:text-red-400 transition-colors p-2 hover:bg-red-500/10 rounded-lg"
                              title="Delete Student"
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {tableData.length > 0 && (
              <div className="px-8 py-4 border-t border-white/5 bg-white/5 flex justify-between items-center">
                <div className="text-xs text-gray-500 font-medium">
                  Showing <span className="text-white font-bold">{indexOfFirstItem + 1}</span> to <span className="text-white font-bold">{Math.min(indexOfLastItem, tableData.length)}</span> of <span className="text-white font-bold">{tableData.length}</span> students
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={prevPage}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-white/10 rounded-xl text-xs font-bold text-gray-400 hover:bg-white/5 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    Previous
                  </button>
                  <button
                    onClick={nextPage}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 bg-accent-purple text-white border border-accent-purple rounded-xl text-xs font-bold shadow-[0_0_10px_rgba(139,92,246,0.3)] hover:bg-accent-purple/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <StudentModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleModalSubmit}
        initialData={editingStudent}
        departments={departments}
        batches={batches}
      />
    </div >
  );
};

export default ManageStudents;
