<?php
// Seeds a sample CS101 course with pages, assignments, an announcement and a test student.
// Run inside the Moodle container (see README "Sample data"):
//   STUDENT_USERNAME=... STUDENT_PASSWORD=... php /tmp/seed_sample_course.php
// Safe to re-run: it stops if a course with short name CS101 already exists.

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->libdir . '/testing/generator/lib.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/mod/assign/locallib.php');
require_once($CFG->dirroot . '/mod/forum/lib.php');

\core\session\manager::set_user(get_admin());

if ($DB->record_exists('course', ['shortname' => 'CS101'])) {
    cli_writeln('CS101 already exists, nothing to do.');
    exit(0);
}
$username = getenv('STUDENT_USERNAME') ?: 'student1';
$password = getenv('STUDENT_PASSWORD');
if (!$password) {
    cli_error('Set STUDENT_PASSWORD');
}

$gen = testing_util::get_data_generator();
$day = 86400;
$now = time();

$course = $gen->create_course([
    'fullname' => 'Intro to Programming',
    'shortname' => 'CS101',
    'numsections' => 3,
    'summaryformat' => FORMAT_HTML,
    'summary' => '<p><b>Instructor:</b> Dr. Ramos. <b>Office hours:</b> Tue/Thu 2-4pm, Room 210.</p>'
        . '<p><b>Grading:</b> Quizzes 20%, Labs 40%, Midterm 15%, Final project 25%.</p>'
        . '<p><b>Late work:</b> -10% per day, up to 3 days. After that, no credit unless you email the instructor before the deadline.</p>'
        . '<p><b>AI tools:</b> You may use AI assistants to explain concepts and debug errors. You may not submit AI-written code as your own.</p>',
]);

foreach ([1 => 'Week 1: Getting Started', 2 => 'Week 2: Loops', 3 => 'Week 3: Functions'] as $num => $title) {
    $section = $DB->get_record('course_sections', ['course' => $course->id, 'section' => $num]);
    course_update_section($course, $section, ['name' => $title]);
}

$page = function (int $section, string $name, string $html) use ($gen, $course) {
    return $gen->create_module('page', [
        'course' => $course->id, 'section' => $section, 'name' => $name,
        'content' => $html, 'contentformat' => FORMAT_HTML,
    ]);
};
$page(1, 'Installing Python',
    '<p>Download Python 3 from python.org. On Mac, run the installer, then open Terminal and type '
    . '<code>python3 --version</code> to check it worked.</p>');
$page(2, 'Loops lecture notes',
    '<p>A <b>for loop</b> repeats code once for each item in a sequence: <code>for i in range(5): print(i)</code> prints 0 through 4.</p>'
    . '<p>A <b>while loop</b> repeats while a condition is true. A <b>loop counter</b> is a variable you update each time through the loop, like <code>count = count + 1</code>.</p>'
    . '<p>Common bug: forgetting to update the counter in a while loop causes an infinite loop.</p>');
$page(3, 'Functions lecture notes',
    '<p>A <b>function</b> is a named block of code you can reuse: <code>def greet(name): return "Hi " + name</code>.</p>'
    . '<p><b>Parameters</b> are the inputs in the definition; <b>arguments</b> are the values you pass when calling it. '
    . '<code>return</code> sends a value back; a function without return gives back <code>None</code>.</p>');

$assign = function (int $section, string $name, string $html, int $due, int $points) use ($gen, $course) {
    return $gen->create_module('assign', [
        'course' => $course->id, 'section' => $section, 'name' => $name,
        'intro' => $html, 'introformat' => FORMAT_HTML,
        'duedate' => $due, 'allowsubmissionsfromdate' => 0, 'cutoffdate' => 0, 'gradingduedate' => 0,
        'grade' => $points, 'assignsubmission_onlinetext_enabled' => 1, 'assignsubmission_file_enabled' => 1,
        'submissiondrafts' => 0,
    ]);
};
$quiz = $assign(1, 'Python Basics Check',
    '<p>Answer the 5 short questions on installing Python and printing output.</p>', $now - 5 * $day, 10);
$reflection = $assign(1, 'Reading Reflection 1',
    '<p>Write one paragraph on why you are taking this course.</p>', $now - 3 * $day, 5);
$lab = $assign(2, 'Lab 1: Loops',
    '<p>Write a program that asks the user for a number n, then prints the sum of all numbers from 1 to n using a loop. '
    . 'Then extend it to print only the even numbers\' sum. Submit your .py file.</p>', $now + 3 * $day, 25);
$assign(3, 'Lab 2: Functions',
    '<p>Rewrite Lab 1 as a function <code>sum_to(n, even_only=False)</code> and call it three times with different inputs.</p>',
    $now + 10 * $day, 25);

// Test student, enrolled in the course.
$student = $gen->create_user([
    'username' => $username, 'password' => $password,
    'firstname' => 'Test', 'lastname' => 'Student', 'email' => $username . '@example.com',
]);
$gen->enrol_user($student->id, $course->id, 'student');

// The student submitted the basics check (a day late) and got a grade; the reflection stays missing.
$cm = get_coursemodule_from_instance('assign', $quiz->id);
$a = new assign(context_module::instance($cm->id), $cm, $course);
$submission = $a->get_user_submission($student->id, true);
$submission->status = ASSIGN_SUBMISSION_STATUS_SUBMITTED;
$submission->timemodified = $now - 4 * $day;
$DB->update_record('assign_submission', $submission);
$a->save_grade($student->id, (object) ['grade' => 7, 'attemptnumber' => 0]);

// Announcement in the course's news forum.
$news = forum_get_course_forum($course->id, 'news');
$gen->get_plugin_generator('mod_forum')->create_discussion([
    'course' => $course->id, 'forum' => $news->id, 'userid' => get_admin()->id,
    'name' => 'Lab 1 due date reminder',
    'message' => '<p>Lab 1 is due in 3 days. Office hours Thursday are extended to 5pm if you need help with loops.</p>',
]);

cli_writeln("Created course {$course->id} (CS101) and student '{$username}'.");
