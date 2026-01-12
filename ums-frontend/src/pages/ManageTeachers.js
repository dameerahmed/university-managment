import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Sidebar from '../components/Sidebar';
import { Search, Filter, ChevronDown, User, BookOpen, Layers, Plus, Edit, Trash2, GraduationCap } from 'lucide-react';
import TeacherModal from '../components/TeacherModal';

const ManageTeachers = () => {
    // --- 1. DATA HOLDING STATES ---
    const [teachers, setTeachers] = useState([]);
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(false);

    // --- 2. FILTER STATES ---
    const [searchQuery, setSearchQuery] = useState('');

    // --- 3. PAGINATION STATES ---
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 8;

    // --- 4. MODAL STATES ---
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingTeacher, setEditingTeacher] = useState(null);

    // --- 5. INITIAL DATA FETCHING ---
    useEffect(() => {
        fetchTeachers();
    }, []);

    const fetchTeachers = async () => {
        setLoading(true);
        try {
            const response = await api.get('/teachers/get_all');
            setTeachers(response.data);
            setTableData(response.data);
        } catch (err) {
            console.error("Failed to fetch teachers:", err);
        } finally {
            setLoading(false);
        }
    };

    // --- 6. SEARCH LOGIC ---
    useEffect(() => {
        if (!searchQuery) {
            setTableData(teachers);
            return;
        }
        const lowerQuery = searchQuery.toLowerCase();
        const filtered = teachers.filter(teacher =>
            (teacher.first_name?.toLowerCase() || '').includes(lowerQuery) ||
            (teacher.last_name?.toLowerCase() || '').includes(lowerQuery) ||
            (teacher.email?.toLowerCase() || '').includes(lowerQuery)
        );
        setTableData(filtered);
        setCurrentPage(1); // Reset to first page on search
    }, [searchQuery, teachers]);


    // --- 7. CRUD HANDLERS ---
    const handleCreate = () => {
        setEditingTeacher(null);
        setIsModalOpen(true);
    };

    const handleEdit = (teacher) => {
        setEditingTeacher(teacher);
        setIsModalOpen(true);
    };

    const handleDelete = async (email) => {
        if (!window.confirm("Are you sure you want to delete this teacher?")) return;
        try {
            await api.delete(`/teachers/delete/${email}`);
            alert("Teacher deleted successfully");
            fetchTeachers();
        } catch (err) {
            console.error("Delete failed:", err);
            alert("Failed to delete teacher");
        }
    };

    const handleModalSubmit = async (formData) => {
        try {
            if (editingTeacher) {
                await api.put(`/teachers/update/${editingTeacher.email}`, formData);
                alert("Teacher updated successfully");
            } else {
                await api.post('/teachers/create', formData);
                alert("Teacher created successfully");
            }
            fetchTeachers();
        } catch (err) {
            console.error("Operation failed:", err);
            throw new Error(err.response?.data?.detail || "Operation failed");
        }
    };

    // --- 8. PAGINATION LOGIC ---
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
                    <div className="absolute top-[20%] left-[30%] w-[500px] h-[500px] bg-accent-purple/10 rounded-full blur-[150px]"></div>
                </div>

                <div className="relative z-10">
                    {/* HEADER SECTION */}
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
                        <div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">
                                Manage Teachers
                            </h1>
                            <p className="text-gray-400 mt-1">Oversee and manage faculty members.</p>
                        </div>
                        <div className="hidden md:block">
                            <button
                                onClick={handleCreate}
                                className="bg-accent-purple hover:bg-accent-purple/90 text-white font-bold py-3 px-6 rounded-xl shadow-[0_0_20px_rgba(139,92,246,0.3)] transition-all flex items-center gap-2 transform hover:-translate-y-0.5 active:scale-95"
                            >
                                <Plus size={20} /> Add Teacher
                            </button>
                        </div>
                    </div>

                    {/* SEARCH & FILTER BAR */}
                    <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-3xl shadow-2xl mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-100">
                        <div className="flex flex-col md:flex-row gap-4 items-center">

                            {/* Search Input */}
                            <div className="relative flex-1 w-full">
                                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-accent-purple" size={20} />
                                <input
                                    type="text"
                                    placeholder="Search by name or email..."
                                    className="w-full pl-12 pr-4 py-3 bg-dark-800/50 border border-white/10 rounded-xl focus:ring-1 focus:ring-accent-purple focus:border-accent-purple focus:bg-dark-800 transition-all outline-none text-gray-200 font-medium placeholder:text-gray-500"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    {/* TABLE SECTION */}
                    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-500 delay-200 shadow-2xl">
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-white/5 border-b border-white/5">
                                    <tr>
                                        <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Name</th>
                                        <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Email</th>
                                        <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Phone</th>
                                        <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Hire Date</th>
                                        <th className="px-8 py-5 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-white/5">
                                    {loading ? (
                                        <tr>
                                            <td colSpan="5" className="text-center py-12">
                                                <div className="flex justify-center items-center gap-3 text-gray-400">
                                                    <div className="w-5 h-5 border-2 border-accent-purple border-t-transparent rounded-full animate-spin"></div>
                                                    Loading teachers...
                                                </div>
                                            </td>
                                        </tr>
                                    ) : tableData.length === 0 ? (
                                        <tr>
                                            <td colSpan="5" className="text-center py-16">
                                                <div className="flex flex-col items-center gap-3 text-gray-500">
                                                    <div className="p-4 bg-white/5 rounded-full">
                                                        <GraduationCap size={32} className="text-gray-600" />
                                                    </div>
                                                    <p className="font-medium text-sm">No teachers found matching your criteria.</p>
                                                </div>
                                            </td>
                                        </tr>
                                    ) : (
                                        currentItems.map((teacher, index) => (
                                            <tr key={teacher.teacher_id} className="hover:bg-white/5 transition-colors group">
                                                <td className="px-8 py-4 whitespace-nowrap">
                                                    <div className="flex items-center gap-4">
                                                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-purple/20 to-accent-pink/20 text-accent-pink flex items-center justify-center font-bold text-lg border border-white/10">
                                                            {teacher.first_name?.[0] || '?'}
                                                        </div>
                                                        <div>
                                                            <div className="font-bold text-gray-200 group-hover:text-white transition-colors">{teacher.first_name} {teacher.last_name}</div>
                                                            <div className="text-xs text-gray-500 font-medium">ID: {teacher.teacher_id}</div>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td className="px-8 py-4 whitespace-nowrap">
                                                    <div className="text-sm font-medium text-gray-300">{teacher.email}</div>
                                                </td>
                                                <td className="px-8 py-4 whitespace-nowrap">
                                                    <div className="text-sm font-medium text-gray-300">{teacher.phone_number}</div>
                                                </td>
                                                <td className="px-8 py-4 whitespace-nowrap">
                                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-accent-blue/10 text-accent-blue border border-accent-blue/20">
                                                        {new Date(teacher.hire_date).toLocaleDateString()}
                                                    </span>
                                                </td>
                                                <td className="px-8 py-4 whitespace-nowrap">
                                                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                        <button
                                                            onClick={() => handleEdit(teacher)}
                                                            className="text-gray-400 hover:text-accent-purple transition-colors p-2 hover:bg-accent-purple/10 rounded-lg"
                                                            title="Edit Teacher"
                                                        >
                                                            <Edit size={16} />
                                                        </button>
                                                        <button
                                                            onClick={() => handleDelete(teacher.email)}
                                                            className="text-gray-400 hover:text-red-400 transition-colors p-2 hover:bg-red-500/10 rounded-lg"
                                                            title="Delete Teacher"
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
                                    Showing <span className="text-white font-bold">{indexOfFirstItem + 1}</span> to <span className="text-white font-bold">{Math.min(indexOfLastItem, tableData.length)}</span> of <span className="text-white font-bold">{tableData.length}</span> teachers
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

            <TeacherModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSubmit={handleModalSubmit}
                initialData={editingTeacher}
            />
        </div >
    );
};

export default ManageTeachers;
